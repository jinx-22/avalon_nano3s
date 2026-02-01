
<img width="100" height="100" alt="logo" src="https://github.com/user-attachments/assets/a0fa0a03-ac01-46dd-a215-0b93cd77d4fc" /> 

# "Avalon Nano 3S" Integration für Home Assistant! 




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

Die Intergration könnte auch mit anderen Firmwarversionen oder auch mit dem Nano 3 kompatibel sein, dies kann ich mangels Gerät nicht testen, daher ist Feedback gewünscht!

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

### Manuell

1. Repository klonen:  
   ```
   git clone https://github.com/jinx-22/avalon_nano3s custom_components/avalon_nano3s
   ```
2. Home Assistant neu starten
3. Integration über **Einstellungen → Geräte & Dienste → Integration hinzufügen**
4. IP-Adresse des Miners und ggf. Passwort des Miners eingeben -> OK

---

### Support, Spenden und Unterstützung! 

Wenn dir meine Arbeit gefällt und sie für dich einen Nutzen und Wert hat, freue ich mich über eine kleine Unterstützung:

## <span style="color: orange; font-size: 1.4em;">₿</span>  Bitcoin: 
``` 
bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry
```
<img width="160" height="162" alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />

## ⚡Lightning : 
```
toughnote102@walletofsatoshi.com
```
<img width="160" height="180" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/d1f63d0d-33ef-4b32-ad14-23f5b6dbd131" />

**Vielen Dank** ,und gebt mir einen kostenlosen [![GitHub stars](https://img.shields.io/github/stars/jinx-22/avalon_nano3s?style=social)](https://github.com/jinx-22/avalon_nano3s/stargazers), dann finden andere auch den Weg hierher - Danke!


---

### 🐛 Bugs / Feature Requests

Bitte direkt auf GitHub:

https://github.com/jinx-22/avalon_nano3s/issues

---


### Lizens


**Apache License 2.0**  -> [Lizens (Volltext)](https://www.apache.org/licenses/LICENSE-2.0)

---


