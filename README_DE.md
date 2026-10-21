<img width="128" height="128" alt="logo" src="https://github.com/jinx-22/avalon_nano3s/blob/main/logos/nano3s_icon.png" />

## Avalon Nano 3S - Integration für Home Assistant (deutsch)
🇬🇧 [**English**](README.md) · 🇩🇪 **Deutsch**



---
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-blue?style=flat-square)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Release](https://img.shields.io/github/v/release/jinx-22/avalon_nano3s?sort=semver&style=flat-square)](https://github.com/jinx-22/avalon_nano3s/releases)
[![License](https://img.shields.io/github/license/jinx-22/avalon_nano3s?style=flat-square)](LICENSE)
[![Usage](https://img.shields.io/badge/dynamic/json?style=flat-square&logo=home-assistant&logoColor=white&label=Usage&suffix=%20installs&color=dc3545&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.avalon_nano3s.total)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=avalon_nano3s&category=integration)
[![stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s)](https://github.com/jinx-22/avalon_nano3s/stargazers)
[![Donate Bitcoin](https://img.shields.io/badge/₿-Bitcoin-F7931A?style=flat-square)](#bitcoin)
[![Donate Lightning](https://img.shields.io/badge/⚡-Lightning-FFD700?style=flat-square)](#lightning) 

**Avalon Nano 3S** ist eine **Home Assistant Integration** für den Canaan Avalon Nano 3S ASIC Miner.  


- 230 Sensoren (ca. 60 aktiv)
  - gefundene Blöcke
  - bester Share
  - Leistung
  - Temperaturen
  - ASIC Chip Frequenz
  - etc...

- Workmode-Steuerung (Low/Mid/High)  
- Steuerung der LED-Farbe, Helligkeit und Effekte
- Lüfter-Gschwindigkeitsregler für manuelle Steuerung hinzugefügt -> 15% (560rpm) - 100% (4660rpm) (V1.1.0.0)
- Reboot-Button
- Button für Zurückstellung zum Lüfter-Auto-Modus (v1.1.0.0)
- Pool Konfigurationsdaten ändern! (Passwort erforderlich!)
- Aktiven Pool (1-3) wechseln "kein Neustart erforderlich!" (V1.2.0.0)
  Hinweis: Nach der Auswahl muss ca. 140 Sekunden gewartet werden, bis der Wechsel vollständig übernommen wurde.

---

### Version 1.2.2.0

Behoben:
* Beim Wechsel des Pools wird nun im Auswahlmenü „Bitte warten → Poolwechsel“ angezeigt. Der Wechsel ist abgeschlossen, sobald die Anzeige wieder zum zuvor ausgewählten „Pool X“ zurückwechselt!
* Wenn der Miner ausgeschaltet oder nicht erreichbar ist, wird die Integration nicht mehr als fehlerhaft markiert. (Diesmal wirklich behoben!)

### Version 1.2.1.0

Behoben:
- Fehlerbehandlung der Avalon-Nano-3S-API überarbeitet.
- Ist der Miner ausgeschaltet oder nicht erreichbar, wird die Integration nicht mehr als fehlerhaft markiert. (funktioniert erst in 1.2.2.0)
- Die normale Home-Assistant-Error-Meldung beim fehlgeschlagenen Datenabruf erscheint weiterhin und ist so gewollt.
- Beim wieder eingeschalteten und erreichbaren Miner funktioniert die Aktualisierung automatisch wieder.


Version 1.2.0.3

Behoben:
- Korrekte Zuordnung der Pool-Indizes in der Pool-Auswahl-Entity. 
  (Hinweis: Nach Wechsel braucht der Nano3s ca. 140 Sekunden)

- Pool-IDs aus der CGMiner-API werden jetzt korrekt den konfigurierten Pool-Einträgen zugeordnet.

Version 1.2.0.2

- Fan-Steuerung von Slider auf NumberMode.BOX umgestellt -> Eingabefeld mit + / – statt Slider

Version 1.2.0.1

- „Ping zum Pool“ korrigiert
- Lüfter-Wert in % bleibt nach Änderung bestehen bis zur nächsten Aktualisierung!
- einige Fehler in den Übersetzungen behoben
- Möglichkeit hinzugefügt, den aktiven Pool (1-3) zu wechseln (kein Neustart erforderlich!)
  Hinweis: Nach der Auswahl muss ca. 140 Sekunden gewartet werden, bis der Wechsel vollständig übernommen wurde.

Version 1.1.0.0
Zwei neue Entitäten:
- Lüfter-Gschwindigkeitsregler für manuelle Steuerung hinzugefügt -> 15% (560rpm) - 100% (4660rpm).
- Button für Zurückstellung zum Lüfter-Auto-Modus hinzugefügt.
#### Vorsicht: Die Temperatur im Auge behalten! Benuzung auf eigenes Risiko!!!

**Hinweis:**
Wenn ich den Nano 3s Lüfter auf 50% stelle: 

- Hashrate nimmt +0,05 TH/s zu. -> Mein Nano3s läuft nach ausgibigen Tests nun mit 6,64- 6,68 TH/s
- ASIC MAX ca 74-79 °C (verlängert die Lebensdauer!)
  Am besten eine Automatition das die Temp nicht über 80 geht!
---

- Version 1.0.0.1 (readme.md aktualisiert für HACS)
- Version: 1.0.0.0 Erstes release

---

Getestete Geräte:

### - Avalon Nano 3S - funktioniert! (Firmware 25061101_97e23a6)
- Avalon Nano 3 - Nur sensoren
- Avalon Q - Sensoren, Lüftergeschwindigkeit, Lüfter-Auto-Modus, Reboot
- Avalon Mini - only sensors - ????? -> no Feedback

**Hinweis**:

Die Intergration könnte auch mit anderen Firmwarversionen kompatibel sein, dies kann ich mangels Gerät nicht testen, daher ist Feedback gewünscht!
Mit "Avalon Nano 3" funktioniert mit dieser Integration nur die Sensoren nicht der Workmode!

---

### Übersicht

Diese Integration erlaubt die vollständige Überwachung und Steuerung des **Avalon Nano 3S Miners** direkt in Home Assistant.  

Funktionen:

- Live-Statistiken des Miners (Temperatur, Lüfter, Hashrate, Energieverbrauch)
- Steuerung des Lüfters -> 15% (560rpm) - 100% (4660rpm) - (Update 1.1.0.0)
- Zurückstellung zum Lüfter-Auto-Modus
- Steuerung der **LEDs** (RGB-Farben, Helligkeit, Effekt)
- Auswahl des Mining **Workmodes** (Low, Mid, High)
- Reboot-Button für den Miner direkt aus HA
- Aktiven Pool (1-3) wechseln im laufenden Betrieb (kein Neustart erforderlich!)
  Hinweis: Nach der Auswahl muss ca. 140 Sekunden gewartet werden, bis der Wechsel vollständig übernommen wurde.
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
<code>usefulplay52@walletofsatoshi.com</code>
<br>
<img height="450" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
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

<img height="500" alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
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
# Haftungsausschluss
Dies ist ein privates Open-Source-Projekt und kein offizielles Produkt vom Gerätehersteller. Benutzung auf eigene Gefahr.

---

