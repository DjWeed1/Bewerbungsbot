# Bewerbungsbot 🤖

[🇩🇪 Deutsch](#🇩🇪-installation--benutzung) | [🇬🇧 English](#🇬🇧-installation--usage)

---

## 🇩🇪 Installation & Benutzung

🔥 **NEU: Lokale Web-Oberfläche (Empfohlen)**
Du kannst den Bot jetzt über eine lokale Web-Oberfläche in deinem Browser bedienen.

1. Lade die Dateien aus diesem Repository herunter.
2. Starte `start_webui.bat`.
3. Die Oberfläche läuft lokal auf `http://127.0.0.1:5000`.
4. Lebenslauf und Stellenanzeigen können lokal ausgewählt bzw. per Drag & Drop verarbeitet werden.

### Sicherheit beim E-Mail-Versand
Der Bot startet standardmäßig im Testmodus. Für echten Versand müssen **zwei** Schalter ausdrücklich aktiviert werden:

```env
SEND_REAL_EMAILS=True
ALLOW_REAL_EMAILS=True
```

`ALLOW_REAL_EMAILS` ist die zusätzliche Sicherheitsfreigabe. Für Tests bleibt `SEND_REAL_EMAILS=False` und/oder `ALLOW_REAL_EMAILS=False`.

### Voraussetzungen
- Python 3.11

### Installation
```bash
python setup_bewerbungsbot.py
```

Alternativ manuell:
```bash
pip install pandas beautifulsoup4 chardet python-dotenv colorama openpyxl
```

### Jobangebote sammeln
Speichere passende Stellenanzeigen als HTML-Dateien im Ordner `anzeigen/`. Der Bot extrahiert daraus E-Mail-Adressen und kann Bewerbungen vorbereiten bzw. – nur bei ausdrücklich aktivierten Versand-Schaltern – versenden.

### Beispielstruktur
```text
Bewerbungsbot/
├── Bewerbungsbot_Template.py
├── setup_bewerbungsbot.py
├── .env                 # niemals committen
├── lebenslauf.pdf       # niemals committen
├── anzeigen/            # lokale Stellenanzeigen
└── Bewerbungen.xlsx     # lokales Bewerbungsprotokoll
```

### `.env`
```env
EMAIL_USER=dein.email@gmail.com
EMAIL_PASS=deinAppPasswort
SEND_REAL_EMAILS=False
ALLOW_REAL_EMAILS=False
```

> Für Gmail wird ein App-Passwort benötigt. Niemals Zugangsdaten, CVs, Zeugnisse oder lokale Bewerbungsdaten in Git committen.

### Änderungsprotokoll
- **28.09.2026, 03:xx Europe/Vienna — Security / Maintenance:** Lokale Zugangsdaten, Bewerbungsdaten, PDFs, Logs und Stellenanzeigen werden über `.gitignore` vom Repository ferngehalten; die Dokumentation wurde an den zweistufigen Sicherheitsmechanismus für echten E-Mail-Versand angepasst.

---

## 🇬🇧 Installation & Usage

🔥 **NEW: Local Web UI (Recommended)**
The bot can be operated through a local browser UI.

### Email sending safety
The bot stays in test mode by default. Real sending requires **both** switches to be explicitly enabled:

```env
SEND_REAL_EMAILS=True
ALLOW_REAL_EMAILS=True
```

`ALLOW_REAL_EMAILS` is the additional safety gate. For testing, keep `SEND_REAL_EMAILS=False` and/or `ALLOW_REAL_EMAILS=False`.

### Requirements
- Python 3.11

### Install
```bash
python setup_bewerbungsbot.py
```

Or manually:
```bash
pip install pandas beautifulsoup4 chardet python-dotenv colorama openpyxl
```

### Security
Never commit `.env`, passwords, CVs, certificates, application spreadsheets, logs, or locally saved job advertisements. See `SECURITY.md` for the security baseline.

### Change log
- **28 Sep 2026, 03:xx Europe/Vienna — Security / Maintenance:** Added repository-level ignores for credentials and local application data and updated the documentation for the two-step real-email safety gate.
