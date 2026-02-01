from __future__ import annotations
import asyncio
import re
import logging
from typing import Dict, Any, Optional
from .const import DEFAULT_PORT, DEFAULT_TIMEOUT, DEFAULT_WEB_USER, DEFAULT_WEB_PASSWORD

_LOGGER = logging.getLogger(__name__)

class AsyncAvalonAPI:
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


    async def _send_raw(self, message: str) -> Optional[str]:
        """Send raw command and return response – no response logging"""
        last_exception = None
        for attempt in range(self.retries + 1):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port),
                    timeout=self.timeout,
                )
                writer.write(message.encode("utf-8"))
                await writer.drain()
                raw = b""
                while True:
                    chunk = await reader.read(4096)
                    if not chunk:
                        break
                    raw += chunk
                writer.close()
                await writer.wait_closed()
                decoded = raw.decode("utf-8", errors="ignore").strip()
                return decoded
            except Exception as e:
                last_exception = e
                if attempt < self.retries:
                    await asyncio.sleep(0.5)

        if last_exception:
            _LOGGER.warning("Connection failed for command '%s' after %d attempts: %s",
                            message, self.retries + 1, last_exception)
        return None

    def _parse_generic(self, data: Optional[str]) -> Dict[str, Any]:
        """Improved, robust parser for CGMiner API responses"""
        if not data or "|" not in data:
            return {}
        sections: Dict[str, Any] = {}
        parts = data.split("|")
        # First part = STATUS
        status_part = parts[0].strip()
        if status_part:
            status_values = {}
            for token in status_part.split(","):
                token = token.strip()
                if "=" in token:
                    k, v = token.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    try:
                        if v.isdigit():
                            status_values[k] = int(v)
                        elif '.' in v and v.replace('.', '', 1).isdigit():
                            status_values[k] = float(v)
                        else:
                            status_values[k] = v
                    except Exception:
                        status_values[k] = v
            sections["STATUS"] = status_values
        # Remaining sections
        for part in parts[1:]:
            part = part.strip()
            if not part:
                continue
            values = {}
            section_name = None
            tokens = part.split(",")
            first_token = tokens[0].strip()
            if "=" in first_token:
                name_key, name_val = first_token.split("=", 1)
                if name_key == "POOL":
                    section_name = "POOL"
                    values["POOL"] = name_val.strip()
                    tokens = tokens[1:]
            else:
                section_name = first_token
            for token in tokens:
                token = token.strip()
                if "=" not in token:
                    continue
                k, v = token.split("=", 1)
                k = k.strip()
                v = v.strip()
                try:
                    if v.isdigit():
                        values[k] = int(v)
                    elif '.' in v and v.replace('.', '', 1).isdigit():
                        values[k] = float(v)
                    else:
                        values[k] = v
                except Exception:
                    values[k] = v
            if not section_name and values:
                section_name = next(iter(values))
            if section_name:
                if section_name in sections:
                    if isinstance(sections[section_name], list):
                        sections[section_name].append(values)
                    else:
                        sections[section_name] = [sections[section_name], values]
                else:
                    sections[section_name] = values
        return sections

    async def _command(self, cmd: str, param: Optional[str] = None) -> Dict[str, Any]:
        raw_cmd = cmd if param is None else f"{cmd}|{param}"
        raw = await self._send_raw(raw_cmd)
        if not raw:
            return {"success": False, "message": "No response from miner", "raw": None}

        parsed = self._parse_generic(raw)
        status = parsed.get("STATUS", {})
        if isinstance(status, list) and status:
            status = status[0]
        success = status.get("STATUS") == "S"
        message = status.get("Msg", "No message")
        return {
            "success": success,
            "message": message,
            "raw": raw,
            "parsed": parsed
        }

    async def version(self) -> Dict[str, Any]:
        return (await self._command("version"))["parsed"]

    async def summary(self) -> Dict[str, Any]:
        return (await self._command("summary"))["parsed"]

    async def stats(self) -> Dict[str, Any]:
        return (await self._command("stats"))["parsed"]

    async def devs(self) -> Dict[str, Any]:
        return (await self._command("devs"))["parsed"]

    async def pools(self) -> Dict[str, Any]:
        result = await self._command("pools")
        data = result["parsed"]
        pools_dict = {}
        pool_list = data.get("POOL", [])
        if isinstance(pool_list, dict):
            pool_list = [pool_list]
        for i, pool in enumerate(pool_list, start=1):
            pools_dict[f"p{i}"] = pool
        return pools_dict

    async def estats(self) -> Dict[str, Any]:
        raw = await self._send_raw("estats")
        if not raw or "|" not in raw:
            return {}
        data_part = raw.split("|", 1)[1].strip()
        estats: Dict[str, Any] = {"temperatures": {}, "fans": {}, "PS": {}, "led": {}, "misc": {}}
        pattern = re.compile(r"(\w+)\[([^\]]*)\]")
        for match in pattern.finditer(data_part):
            key, val = match.group(1), match.group(2).strip()
            if key in {"ITemp", "OTemp", "TMax", "TAvg", "TarT", "MTmax", "MTavg"}:
                try:
                    estats["temperatures"][key] = float(val)
                except Exception:
                    estats["temperatures"][key] = None
            elif key.startswith("Fan"):
                try:
                    estats["fans"][key] = int(val.replace("%", "")) if val else None
                except Exception:
                    estats["fans"][key] = None
            elif key == "PS":
                parts = [p.strip() for p in val.split() if p.strip()]
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
                        estats["PS"] = {"raw": val, "parse_error": True}
                else:
                    estats["PS"] = {"raw": val, "too_few_fields": True}
            elif key == "LED":
                try:
                    estats["led"]["LED"] = int(val)
                except Exception:
                    estats["led"]["LED"] = None
            elif key == "LEDUser":
                try:
                    parts = [p.strip() for p in val.split("-") if p.strip()]
                    if len(parts) >= 6:
                        estats["led"]["LEDUser"] = {
                            "Effect": int(parts[0]),
                            "Brightness": int(parts[1]),
                            "ColorTemp": int(parts[2]),
                            "R": int(parts[3]),
                            "G": int(parts[4]),
                            "B": int(parts[5]),
                            "raw": val
                        }
                    else:
                        estats["led"]["LEDUser"] = {"raw": val, "incomplete": True}
                except Exception as e:
                    estats["led"]["LEDUser"] = {"raw": val, "error": str(e)}
            elif key == "WORKMODE":
                try:
                    estats["WORKMODE"] = int(val)
                except Exception:
                    estats["WORKMODE"] = None
            else:
                estats["misc"][key] = val
        return estats

    async def set_workmode(self, level: int) -> Dict[str, Any]:
        return await self._command("ascset", f"0,workmode,set,{level}")

    async def set_led(self, effect: int, bright: int, temper: int, r: int, g: int, b: int) -> Dict[str, Any]:
        bright = max(5, min(100, int(bright)))
        param = f"0,ledset,{effect}-{bright}-{temper}-{r}-{g}-{b}"
        return await self._command("ascset", param)

    async def reboot(self) -> Dict[str, Any]:
        return await self._command("ascset", "0,reboot,0")

    async def set_pool(self, pool_index: int, url: str, user: str, password: str) -> dict:
        if pool_index in (1, 2, 3):
            pool_num = pool_index - 1
        else:
            pool_num = pool_index

        web_user = self.web_user
        web_pass = self.web_password
        param = f"{web_user},{web_pass},{pool_num},{url},{user},{password}"
        raw_cmd = f"setpool|{param}"
        raw_result = await self._send_raw(raw_cmd)
        if not raw_result:
            return {"success": False, "message": "No response from miner", "raw": None}

        parsed = self._parse_generic(raw_result)
        status = parsed.get("STATUS", {})
        if isinstance(status, list) and status:
            status = status[0]
        success = status.get("STATUS") == "S"
        message = status.get("Msg", "No message")
        if not success and ("success" in message.lower() or "set info" in message.lower()):
            success = True
        if success:
            _LOGGER.info("Pool %d set successfully (reboot required): %s", pool_index, message)
        else:
            _LOGGER.error("Failed to set pool %d: %s | Raw: %s", pool_index, message, raw_result)
        return {
            "success": success,
            "message": message,
            "raw": raw_result,
            "parsed": parsed
        }