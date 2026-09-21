from __future__ import annotations

import asyncio
import logging
import re
from typing import Any, Dict, Optional

from .const import (
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_WEB_PASSWORD,
    DEFAULT_WEB_USER,
)

_LOGGER = logging.getLogger(__name__)


class AvalonAPIConnectionError(Exception):
    """Raised when the Avalon Nano 3S cannot be reached."""


class AsyncAvalonAPI:
    """Async API client for Avalon Nano 3S CGMiner API."""

    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = 2,
        web_user: str = DEFAULT_WEB_USER,
        web_password: str = DEFAULT_WEB_PASSWORD,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.web_user = web_user
        self.web_password = web_password

    async def _send_raw(self, message: str) -> str:
        """Send a raw command to the miner and return the response.

        Connection failures are deliberately not logged here.
        The coordinator is responsible for handling availability.
        """

        last_exception: Exception | None = None

        for attempt in range(self.retries + 1):
            reader: asyncio.StreamReader | None = None
            writer: asyncio.StreamWriter | None = None

            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(
                        self.host,
                        self.port,
                    ),
                    timeout=self.timeout,
                )

                writer.write(message.encode("utf-8"))
                await writer.drain()

                raw = bytearray()

                while True:
                    chunk = await asyncio.wait_for(
                        reader.read(4096),
                        timeout=self.timeout,
                    )

                    if not chunk:
                        break

                    raw.extend(chunk)

                return bytes(raw).decode(
                    "utf-8",
                    errors="ignore",
                ).strip()

            except Exception as err:
                last_exception = err

                if attempt < self.retries:
                    await asyncio.sleep(0.5)

            finally:
                if writer is not None:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except Exception:
                        pass

        raise AvalonAPIConnectionError(
            f"Unable to connect to Avalon Nano 3S "
            f"{self.host}:{self.port}"
        ) from last_exception

    def _parse_generic(
        self,
        data: Optional[str],
    ) -> Dict[str, Any]:
        """Parse a generic CGMiner API response."""

        if not data or "|" not in data:
            return {}

        sections: Dict[str, Any] = {}
        parts = data.split("|")

        # First part = STATUS
        status_part = parts[0].strip()

        if status_part:
            status_values: Dict[str, Any] = {}

            for token in status_part.split(","):
                token = token.strip()

                if "=" not in token:
                    continue

                key, value = token.split("=", 1)

                key = key.strip()
                value = value.strip()

                try:
                    if value.isdigit():
                        status_values[key] = int(value)

                    elif (
                        "." in value
                        and value.replace(".", "", 1).isdigit()
                    ):
                        status_values[key] = float(value)

                    else:
                        status_values[key] = value

                except Exception:
                    status_values[key] = value

            sections["STATUS"] = status_values

        # Remaining sections
        for part in parts[1:]:
            part = part.strip()

            if not part:
                continue

            values: Dict[str, Any] = {}
            section_name: str | None = None

            tokens = part.split(",")
            first_token = tokens[0].strip()

            if "=" in first_token:
                name_key, name_value = first_token.split(
                    "=",
                    1,
                )

                if name_key == "POOL":
                    section_name = "POOL"
                    values["POOL"] = name_value.strip()
                    tokens = tokens[1:]

            else:
                section_name = first_token

            for token in tokens:
                token = token.strip()

                if "=" not in token:
                    continue

                key, value = token.split("=", 1)

                key = key.strip()
                value = value.strip()

                try:
                    if value.isdigit():
                        values[key] = int(value)

                    elif (
                        "." in value
                        and value.replace(".", "", 1).isdigit()
                    ):
                        values[key] = float(value)

                    else:
                        values[key] = value

                except Exception:
                    values[key] = value

            if not section_name and values:
                section_name = next(iter(values))

            if section_name:
                if section_name in sections:
                    if isinstance(sections[section_name], list):
                        sections[section_name].append(values)
                    else:
                        sections[section_name] = [
                            sections[section_name],
                            values,
                        ]
                else:
                    sections[section_name] = values

        return sections

    async def _command(
        self,
        cmd: str,
        param: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute a CGMiner API command."""

        raw_cmd = (
            cmd
            if param is None
            else f"{cmd}|{param}"
        )

        raw = await self._send_raw(raw_cmd)

        if not raw:
            raise AvalonAPIConnectionError(
                f"Empty response for command '{cmd}'"
            )

        parsed = self._parse_generic(raw)

        if not parsed:
            raise AvalonAPIConnectionError(
                f"Invalid response for command '{cmd}'"
            )

        status = parsed.get("STATUS", {})

        if isinstance(status, list) and status:
            status = status[0]

        if not isinstance(status, dict):
            status = {}

        success = status.get("STATUS") == "S"
        message = status.get(
            "Msg",
            "No message",
        )

        return {
            "success": success,
            "message": message,
            "raw": raw,
            "parsed": parsed,
        }

    async def version(self) -> Dict[str, Any]:
        """Get miner firmware/version information."""

        result = await self._command("version")
        return result["parsed"]

    async def summary(self) -> Dict[str, Any]:
        """Get miner summary information."""

        result = await self._command("summary")
        return result["parsed"]

    async def stats(self) -> Dict[str, Any]:
        """Get miner statistics."""

        result = await self._command("stats")
        return result["parsed"]

    async def devs(self) -> Dict[str, Any]:
        """Get miner device/ASIC information."""

        result = await self._command("devs")
        return result["parsed"]

    async def pools(self) -> Dict[str, Any]:
        """Get mining pool information."""

        result = await self._command("pools")

        data = result["parsed"]

        pools_dict: Dict[str, Any] = {}

        pool_list = data.get("POOL", [])

        if isinstance(pool_list, dict):
            pool_list = [pool_list]

        for index, pool in enumerate(
            pool_list,
            start=1,
        ):
            pools_dict[f"p{index}"] = pool

        return pools_dict

    async def estats(self) -> Dict[str, Any]:
        """Get extended miner statistics."""

        raw = await self._send_raw("estats")

        if not raw:
            raise AvalonAPIConnectionError(
                "Empty response for command 'estats'"
            )

        if "|" not in raw:
            raise AvalonAPIConnectionError(
                "Invalid response for command 'estats'"
            )

        data_part = raw.split("|", 1)[1].strip()

        estats: Dict[str, Any] = {
            "temperatures": {},
            "fans": {},
            "PS": {},
            "led": {},
            "misc": {},
        }

        pattern = re.compile(
            r"(\w+)\[([^\]]*)\]"
        )

        for match in pattern.finditer(data_part):
            key = match.group(1)
            value = match.group(2).strip()

            if key in {
                "ITemp",
                "OTemp",
                "TMax",
                "TAvg",
                "TarT",
                "MTmax",
                "MTavg",
            }:
                try:
                    estats["temperatures"][key] = float(value)
                except Exception:
                    estats["temperatures"][key] = None

            elif key.startswith("Fan"):
                try:
                    estats["fans"][key] = (
                        int(value.replace("%", ""))
                        if value
                        else None
                    )
                except Exception:
                    estats["fans"][key] = None

            elif key == "PS":
                parts = [
                    part.strip()
                    for part in value.split()
                    if part.strip()
                ]

                if len(parts) >= 7:
                    try:
                        estats["PS"] = {
                            "PS_Status": int(parts[0]),
                            "PS_ControlVoltage": int(parts[1]),
                            "PS_HashboardVoltage": int(parts[2]),
                            "PS_Ping": int(parts[3]),
                            "PS_Reserved": int(parts[4]),
                            "PS_CurrentOutput": int(parts[5]),
                            "PS_Power": int(parts[6]),
                        }
                    except Exception:
                        estats["PS"] = {
                            "raw": value,
                            "parse_error": True,
                        }
                else:
                    estats["PS"] = {
                        "raw": value,
                        "too_few_fields": True,
                    }

            elif key == "LED":
                try:
                    estats["led"]["LED"] = int(value)
                except Exception:
                    estats["led"]["LED"] = None

            elif key == "LEDUser":
                try:
                    parts = [
                        part.strip()
                        for part in value.split("-")
                        if part.strip()
                    ]

                    if len(parts) >= 6:
                        estats["led"]["LEDUser"] = {
                            "Effect": int(parts[0]),
                            "Brightness": int(parts[1]),
                            "ColorTemp": int(parts[2]),
                            "R": int(parts[3]),
                            "G": int(parts[4]),
                            "B": int(parts[5]),
                            "raw": value,
                        }
                    else:
                        estats["led"]["LEDUser"] = {
                            "raw": value,
                            "incomplete": True,
                        }

                except Exception as err:
                    estats["led"]["LEDUser"] = {
                        "raw": value,
                        "error": str(err),
                    }

            elif key == "WORKMODE":
                try:
                    estats["WORKMODE"] = int(value)
                except Exception:
                    estats["WORKMODE"] = None

            else:
                estats["misc"][key] = value

        return estats

    async def set_workmode(
        self,
        level: int,
    ) -> Dict[str, Any]:
        """Set miner work mode."""

        return await self._command(
            "ascset",
            f"0,workmode,set,{level}",
        )

    async def set_fan_speed(
        self,
        speed: int,
    ) -> Dict[str, Any]:
        """Set miner fan speed."""

        if speed != -1:
            speed = max(
                15,
                min(100, int(speed)),
            )

        return await self._command(
            "ascset",
            f"0,fan-spd,{speed}",
        )

    async def set_led(
        self,
        effect: int,
        bright: int,
        temper: int,
        r: int,
        g: int,
        b: int,
    ) -> Dict[str, Any]:
        """Set miner LED."""

        bright = max(
            5,
            min(100, int(bright)),
        )

        param = (
            f"0,ledset,"
            f"{effect}-{bright}-{temper}-"
            f"{r}-{g}-{b}"
        )

        return await self._command(
            "ascset",
            param,
        )

    async def reboot(self) -> Dict[str, Any]:
        """Reboot the miner."""

        return await self._command(
            "ascset",
            "0,reboot,0",
        )

    async def set_pool(
        self,
        pool_index: int,
        url: str,
        user: str,
        password: str,
    ) -> Dict[str, Any]:
        """Configure a mining pool."""

        if pool_index in (1, 2, 3):
            pool_num = pool_index - 1
        else:
            pool_num = pool_index

        web_user = self.web_user
        web_pass = self.web_password

        param = (
            f"{web_user},{web_pass},"
            f"{pool_num},{url},{user},{password}"
        )

        raw_cmd = f"setpool|{param}"

        raw_result = await self._send_raw(raw_cmd)

        if not raw_result:
            raise AvalonAPIConnectionError(
                "Empty response for command 'setpool'"
            )

        parsed = self._parse_generic(raw_result)

        status = parsed.get("STATUS", {})

        if isinstance(status, list) and status:
            status = status[0]

        if not isinstance(status, dict):
            status = {}

        success = status.get("STATUS") == "S"

        message = status.get(
            "Msg",
            "No message",
        )

        if (
            not success
            and (
                "success" in message.lower()
                or "set info" in message.lower()
            )
        ):
            success = True

        if success:
            _LOGGER.info(
                "Pool %d set successfully "
                "(reboot required): %s",
                pool_index,
                message,
            )
        else:
            _LOGGER.error(
                "Failed to set pool %d: %s | Raw: %s",
                pool_index,
                message,
                raw_result,
            )

        return {
            "success": success,
            "message": message,
            "raw": raw_result,
            "parsed": parsed,
        }

    async def switch_pool(
        self,
        pool_index: int,
    ) -> Dict[str, Any]:
        """Switch the active pool without reboot."""

        raw = await self._send_raw(
            f"switchpool|{pool_index}"
        )

        if not raw:
            raise AvalonAPIConnectionError(
                "Empty response for command 'switchpool'"
            )

        parsed = self._parse_generic(raw)

        status = parsed.get("STATUS", {})

        if isinstance(status, list) and status:
            status = status[0]

        if not isinstance(status, dict):
            status = {}

        success = status.get("STATUS") == "S"

        message = status.get(
            "Msg",
            "",
        )

        return {
            "success": success,
            "message": message,
            "raw": raw,
            "parsed": parsed,
        }
