<img width="128" height="128" alt="logo" src="https://github.com/jinx-22/avalon_nano3s/blob/main/logos/nano3s_icon.png" />

# "Avalon Nano 3S" Integration for Home Assistant!
🇬🇧 **English** · 🇩🇪 [**Deutsch**](README_DE.md)
---

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-blue?style=flat-square)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Release](https://img.shields.io/github/v/release/jinx-22/avalon_nano3s?sort=semver&style=flat-square)](https://github.com/jinx-22/avalon_nano3s/releases)
[![License](https://img.shields.io/github/license/jinx-22/avalon_nano3s?style=flat-square)](LICENSE)
[![Usage](https://img.shields.io/badge/dynamic/json?style=flat-square&logo=home-assistant&logoColor=white&label=Usage&suffix=%20installs&color=dc3545&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.avalon_nano3s.total)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=avalon_nano3s&category=integration)
[![stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s)](https://github.com/jinx-22/avalon_nano3s/stargazers)
[![Donate Bitcoin](https://img.shields.io/badge/₿-Bitcoin-F7931A?style=flat-square)](#bitcoin)
[![Donate Lightning](https://img.shields.io/badge/⚡-Lightning-FFD700?style=flat-square)](#lightning)

**Avalon Nano 3S** is a **Home Assistant integration** for the Canaan Avalon Nano 3S ASIC miner.

- 230 sensors (approx. 60 active)
  - Block found
  - best share
  - power
  - Temp´s
  - ASIC chip frequency
  - etc...
  
- Workmode control (Low / Mid / High)
- Control LED color, brightness and effects
- Reboot button
- Auto Fan button ((v1.1.0.0)
- Change pool configuration data (password required!)
- Choose Pool (1-3) connection "without reboot !!!" (v1.2.0.0)
  (Note: after choose you musst wait ca. 140 seconds!)
- Control Fan speed -> 15% (560rpm) - 100% (4660rpm). (V1.1.0.0)
---

### Version 1.2.1.0

Fixed:

* Reworked error handling for the Avalon Nano 3S API.
* When the miner is powered off or unreachable, the integration is no longer marked as faulty.
* The normal Home Assistant error message when a data update fails continues to appear and is intentional.
* When the miner is powered back on and becomes reachable again, updates resume automatically.



Version 1.2.0.3

Fixed:
- Corrected pool index mapping inpool choose (select) entity. 
  (Note: After switching pools, the Nano3S take approximately 140 seconds to complete the switch)

- Pool IDs from CGMiner API are now mapped correctly to configured pool entries.

Version 1.2.0.2

- "Fan control" from slider-entity to NumberMode.BOX  # # Input field with + / - instead of slider

Version 1.2.0.1

- fixed "Ping to Pool"
- fixed stay value after change FAN%
- fixed any bugs in translations
- add choose Pool (1-3) connection "without reboot !!!" -> after choose you musst wait ca. 140 seconds!

Version 1.1.0.0

Two new entitys:
- Add Fan-Speed Slider for manuel Fan control -> 15% (560rpm) - 100% (4660rpm).
- Add Button to go back to Fan-Auto-Modus.

#### Attention : Use it on your own risk!!!

**Note:**
When my Nano 3s Fan to 54%: 

- Hashrate +0,06 TH/s up, with 54% Fan -> My Nano3s up to 6,64 - 6,68 TH/s after few tests!
- ASIC MAX  74-79 °C (Extends the lifespan when under 80)

---

- Version 1.0.0.1 (edit readme.md for HACS)
- Version: 1.0.0.0 first release


Tested so far:

### - Avalon Nano 3S -FINE! (Firmware 25061101_97e23a6)
- Avalon Nano 3 - only sensors
- Avalon Q - only Sensors an Fan-Control
- Avalon Mini - only sensors - no Feedback
---

**Note:**

This integration may also be compatible with other firmware versions — unfortunately I cannot test this without additional hardware, so feedback is welcome!

With the “Avalon Nano 3”, only sensors work using this integration — workmode control does NOT.

---

## Overview

This integration allows full monitoring and control of the **Avalon Nano 3S Miner** directly from Home Assistant.

Features:

- Live miner statistics (temperature, fan, hashrate, power consumption)
- Fan control -> 15% (560rpm) - 100% (4660rpm) - (Update 1.1.0.0)
- Button to go back to Fan-Auto-Modus.
- **LED control** (RGB colors, brightness, effects)
- Mining **workmode** selection (Low, Mid, High)
- Reboot button directly from Home Assistant
- Choose Pool (1-3) connection "without reboot !!!" -> after choose you musst wait ca. 140 seconds!
- Enter/change pool data via the **GUI Config Flow**

---

### Pool Configuration Notes

To change pool data from Home Assistant, the miner login password must be provided during installation or later in the integration options.

The password is ONLY required for pool configuration changes.

If you do not plan to modify pool data via Home Assistant, no password is required.

**Warning:** After changing any pool entry, the miner will automatically reboot!

---

## Installation

### Internal (via HACS)

Registered in HACS:

Simply search for **“Avalon Nano 3S”** in HACS and download — restart Home Assistant — install!

---

### 👉 One-Click Installation

[![Open your Home Assistant instance and add this repository to HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=avalon_nano3s&category=integration)

1. Restart Home Assistant
2. Add integration via **Settings → Devices & Services → Add Integration**
3. Enter miner IP address and optional password → OK

---

### Via HACS (manual)

1. HACS → top right three-dot menu
2. Add custom repository:  
   `https://github.com/jinx-22/avalon_nano3s` and select `Integration`
3. Search for the integration in HACS and install
4. Restart Home Assistant
5. Add integration via **Settings → Devices & Services → Add Integration**
6. Enter miner IP address and optional password → OK

---
## 🧡 Support & Donations

If you like this integration and it adds real value to your Home Assistant setup,  
I’d appreciate a small donation — every contribution helps further development 🚀

## Lightning
<p align="center">
⚡ <b>Address:</b>
<br><br>
<code>usefulplay52@walletofsatoshi.com</code>
<br>

<img height="450" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
<br><br>
or:
<br><br></p>

## Bitcoin
<div align="center">
<img width="100" height="100" alt="Bitcoin_100px" src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" />
<br><br>

<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code>
<br>

<img height="500" alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
<br><br>
</div>

**Thank you very much**, and please leave a free  
[![GitHub stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s?style=social)](https://github.com/jinx-22/avalon_nano3s/stargazers)  
so others can find this project too — thanks!

---

## 🐛 Bugs / Feature Requests

Please open issues directly on GitHub:

https://github.com/jinx-22/avalon_nano3s/issues

---

## License

**Apache License 2.0** → [License (full text)](https://www.apache.org/licenses/LICENSE-2.0)

---

# Disclaimer
This is a private open-source project and not an official product of device manufacturer. Use at your own risk.

---

