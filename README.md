<img width="128" height="128" alt="logo" src="https://github.com/user-attachments/assets/b81e4c9f-ebfc-4289-a25f-4a2e879b2b3e" />

# "Avalon Nano 3S" Integration for Home Assistant!
*Link to German version: [Deutsch](#avalon-nano-3s---integration-für-home-assistant-deutsch)*
---

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-blue)](https://www.home-assistant.io/)  
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)  
[![Release](https://img.shields.io/github/v/release/jinx-22/avalon_nano3s?sort=semver)](https://github.com/jinx-22/avalon_nano3s/releases)  
[![License](https://img.shields.io/github/license/jinx-22/avalon_nano3s)](LICENSE)  
[![Donate BTC](https://img.shields.io/badge/₿-orange?style=flat-square)](bitcoin:bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry)  
[![Donate ⚡](https://img.shields.io/badge/⚡-yellow?style=flat-square)](lightning:toughnote102@walletofsatoshi.com)  
[![stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s)](https://github.com/jinx-22/avalon_nano3s/stargazers)

**Avalon Nano 3S** is a **Home Assistant integration** for the Canaan Avalon Nano 3S ASIC miner.

- 230 sensors (approx. 60 active)
- Workmode control (Low / Mid / High)
- Control LED color, brightness and effects
- Reboot button
- Change pool configuration data (password required!)

---

### Version: 1.0.0.0

Tested so far:

- Avalon Nano 3S (Firmware 25061101_97e23a6)

---

**Note:**

This integration may also be compatible with other firmware versions — unfortunately I cannot test this without additional hardware, so feedback is welcome!

With the “Avalon Nano 3”, only sensors work using this integration — workmode control does NOT.

---

## Overview

This integration allows full monitoring and control of the **Avalon Nano 3S Miner** directly from Home Assistant.

Features:

- Live miner statistics (temperature, fan, hashrate, power consumption)
- **LED control** (RGB colors, brightness, effects)
- Mining **workmode** selection (Low, Mid, High)
- Reboot button directly from Home Assistant
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

<p align="center">
⚡ <b>Lightning Address:</b>
<br><br>
<code>toughnote102@walletofsatoshi.com</code>
<br>

<img width="160" height="180" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/d1f63d0d-33ef-4b32-ad14-23f5b6dbd131" />
<br><br>
or:
<br><br>

<div align="center">
<img width="25" height="25" alt="Bitcoin_25px" src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" />
 Bitcoin:
<br><br>

<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code>
<br>

<img width="160" height="162" alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
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



---
---

<img width="128" height="128" alt="logo" src="https://github.com/user-attachments/assets/b81e4c9f-ebfc-4289-a25f-4a2e879b2b3e" />

## Avalon Nano 3S - Integration für Home Assistant (deutsch)




---
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-blue)](https://www.home-assistant.io/) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)  [![Release](https://img.shields.io/github/v/release/jinx-22/avalon_nano3s?sort=semver)](https://github.com/jinx-22/avalon_nano3s/releases)  [![License](https://img.shields.io/github/license/jinx-22/avalon_nano3s)](LICENSE) [![Donat BTC](https://img.shields.io/badge/₿-orange?style=flat-square)](bitcoin:bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry)
[![Donate ⚡](https://img.shields.io/badge/⚡-yellow?style=flat-square)](lightning:toughnote102@walletofsatoshi.com) [![stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s)](https://github.com/jinx-22/avalon_nano3s/stargazers)

**Avalon Nano 3S** ist eine **Home Assistant Integration** für den Canaan Avalon Nano 3S ASIC Miner.  


- 230 Sensoren (ca. 60 aktiv)  
- Workmode-Steuerung (Low/Mid/High)  
- Steuerung der LED-Farbe, Helligkeit und Effekte  
- Reboot-Button 
- Pool Konfigurationsdaten ändern! (Passwort erforderlich!)
---

### Version: 1.0.0.0 

Bisher getestet:

- Avalon Nano 3s (mit Firmware 25061101_97e23a6)


**Hinweis**:

Die Intergration könnte auch mit anderen Firmwarversionen kompatibel sein, dies kann ich mangels Gerät nicht testen, daher ist Feedback gewünscht!
Mit "Avalon Nano 3" funktioniert mit dieser Integration nur die Sensoren nicht der Workmode!

---

### Übersicht

Diese Integration erlaubt die vollständige Überwachung und Steuerung des **Avalon Nano 3S Miners** direkt in Home Assistant.  

Funktionen:

- Live-Statistiken des Miners (Temperatur, Lüfter, Hashrate, Energieverbrauch)
- Steuerung der **LEDs** (RGB-Farben, Helligkeit, Effekt)
- Auswahl des Mining **Workmodes** (Low, Mid, High)
- Reboot-Button für den Miner direkt aus HA
- Eingabe/Änderung der Pool-Daten über den **GUI Config Flow** <p>

**Hinweis zum ändern der Pool-Daten:**

Für die Änderung von Pool-Daten aus Homeassistant heraus muss das Login-Passwort bei Installation eingegeben werden, oder in den Optionen später nachgetragen werden werden, das Passwort wird nur für die Änderung der Pooldaten benötigt! Wollt ihr die Daten über HA nicht ändern, wird das Passwort nicht benötigt!

**Achtung:** Nach einer Änderung eines Pool-Datensatzes wird der Miner automatisch neu gestartet!

---

### Installation

Intern:
Registriert bei HACS: 
In der Suchleiste von HACS einfach "Avalon Nano 3S" eingeben und herunterladen - Neustart - installieren!

### 👉 One-Click Installation

[![Open your Home Assistant instance and add this repository to HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=avalon_nano3s&category=integration)

2. Home Assistant neu starten
3. Integration über **Einstellungen → Geräte & Dienste → Integration hinzufügen**
4. IP-Adresse des Miners und ggf. Passwort des Miners eingeben -> OK

### Über HACS (manuell)

1. HACS -> oben rechts 3-Punkte-Menü
2. Benutzerdefiniertes Repository zu HACS hinzufügen:  
   `https://github.com/jinx-22/avalon_nano3s` + `Integration` wahlen
3. "Integration" unter HACS suchen und installieren
4. Home Assistant neu starten
5. Integration über **Einstellungen → Geräte & Dienste → Integration hinzufügen**
6. IP-Adresse des Miners und ggf. Passwort des Miners eingeben -> OK

---
## 🧡 Support & Unterstützung

Wenn dir diese Integration gefällt und sie einen echten Mehrwert für dein Home Assistant Setup bietet,  
freue ich mich über eine kleine Unterstützung — jede Spende hilft, das Projekt weiterzuentwickeln 🚀
<br>
<p align="center">
⚡ <b>Lightning Adresse:</b>
<br> <br>
<code>toughnote102@walletofsatoshi.com</code>
<br>
<img width="160" height="180" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/d1f63d0d-33ef-4b32-ad14-23f5b6dbd131" />
<br> <br>
oder: 
<br>
<br>
<div align="center">
<img width="25" height="25" alt="Bitcoin_25px" src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" />
 Bitcoin:
   <br> <br>
  <code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry
  </code>
    <br>

<img width="160" height="162" alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
<br>   <br>
</div>

**Vielen Dank** ,und gebt mir einen kostenlosen [![GitHub stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s?style=social)](https://github.com/jinx-22/avalon_nano3s/stargazers), dann finden andere auch den Weg hierher - Danke!


---

### 🐛 Bugs / Feature Requests

Bitte direkt auf GitHub:

https://github.com/jinx-22/avalon_nano3s/issues

---


### Lizens


**Apache License 2.0**  -> [Lizens (Volltext)](https://www.apache.org/licenses/LICENSE-2.0)

---


