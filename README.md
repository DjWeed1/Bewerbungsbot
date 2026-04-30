# Bewerbungsbot 🤖

[🇩🇪 Deutsch](#🇩🇪-installation--benutzung) | [🇬🇧 English](#🇬🇧-installation--usage)

---

## 🇩🇪 Installation & Benutzung

🔥 **NEU: Lokale Web-Oberfläche (Empfohlen)**
Du kannst den Bot jetzt super einfach über eine moderne Web-Oberfläche in deinem Browser bedienen!
1. Lade dir die Dateien aus diesem Repository herunter.
2. Mache einen Doppelklick auf die Datei **`start_webui.bat`**.
3. Dein Browser öffnet sich automatisch (auf `http://127.0.0.1:5000`).
4. Du kannst deinen Lebenslauf und Stellenanzeigen per Drag & Drop reinziehen, deine Daten eintragen und den Bot per Knopfdruck starten!

*(Wenn du den Bot lieber klassisch über das Terminal nutzen möchtest, folge der Anleitung unten:)*

### 1️⃣ Voraussetzungen
*   **Python 3.11** ist bereits installiert ✅

### 2️⃣ Erforderliche Pakete installieren (oder One-Click-Setup nutzen)
Führe das `setup_bewerbungsbot.py` Script in deiner PowerShell/CMD aus:
```bash
python setup_bewerbungsbot.py
```
*(Alternativ: `py setup_bewerbungsbot.py`)*

Der `setup_bewerbungsbot.py` macht das Setup zum Kinderspiel („One-Click-Setup“):
*   Fragt dich Schritt für Schritt nach deinen Daten.
*   Erstellt die nötige Ordnerstruktur, die `.env` Datei, die Excel-Datei und eine Logdatei.
*   Prüft, ob alle Bibliotheken installiert sind und installiert Fehlendes automatisch.
*   Macht den Bot sofort startfertig und startet ihn auf Wunsch direkt.

Wenn du alles **manuell** installieren möchtest, öffne PowerShell oder CMD und gib ein:
```bash
pip install pandas beautifulsoup4 chardet python-dotenv colorama openpyxl
```

### 3️⃣ Jobangebote sammeln
Gehe auf ein Job-Portal wie z. B. [AMS Jobroom](https://jobroom.ams.or.at/jobsuche/FreieSuche.jsp).
Gehe die Stellenanzeigen durch. Alles, was eine E-Mail-Adresse hat und dir gefällt, speicherst du mit **Rechtsklick > Speichern unter...** in den Ordner `Bewerbungsbot/anzeigen` (als HTML-Datei). 
Wenn du z. B. 100 Anzeigen gespeichert hast und den Bot startest, wird er alle E-Mail-Adressen heraussuchen und überall eine Bewerbung mit deinem Lebenslauf/Zeugnissen usw. hinschicken.

### 4️⃣ Ordnerstruktur anlegen (Wird durch das Setup automatisch erstellt)
Beispiel, wie es aussehen sollte:
```text
C:\Users\User\Documents\Bewerbungsbot\
│
├── Bewerbungsbot_Template.py
├── setup_bewerbungsbot.py
├── .env
├── lebenslauf.pdf
├── anzeigen\                  <-- Hier kommen deine gespeicherten HTML-Anzeigen rein
└── Bewerbungen.xlsx
```

### 5️⃣ .env Datei anlegen (Wird durch das Setup automatisch erstellt)
Erstelle in deinem Hauptordner eine Datei namens `.env` mit folgendem Inhalt:
```env
EMAIL_USER=dein.email@gmail.com
EMAIL_PASS=deinAppPasswort
SEND_REAL_EMAILS=True
```
> **Tipp:** Bei Gmail brauchst du ein App-Passwort (nicht dein normales Passwort!). [Hier erstellen](https://myaccount.google.com/apppasswords).
> Wenn du den Bot nur testen willst (ohne E-Mails zu versenden), setze in der `.env`:
> `SEND_REAL_EMAILS=False`

### 6️⃣ Anpassung
Ersetze im Code (`Bewerbungsbot_Template.py`):
*   `*NAME*` → durch deinen Namen
*   `*ORDNER_HTML*`, `*EXCEL_FILE*`, `*CV_FILE*`, `*ENV_PATH*` → durch deine eigenen Dateipfade

### 7️⃣ Bot Starten
Sobald alles eingerichtet ist, starte den Bot mit:
```bash
python Bewerbungsbot_Template.py
```

### 📞 Kontakt & Support
Bei Problemen kannst du mich gerne über WhatsApp oder Telegram kontaktieren: **+4367762127550** (Lg Pierre).
Für weitere Fragen stehe ich auch in der WhatsApp-Gruppe zur Verfügung: [WhatsApp Gruppe beitreten](https://chat.whatsapp.com/EHw5Ahb4cUDDIEWZfiyI6x). 
Nun viel Glück! 😉

---

## 🇬🇧 Installation & Usage

🔥 **NEW: Local Web UI (Recommended)**
You can now easily control the bot using a modern web interface in your browser!
1. Download the files from this repository.
2. Double-click the **`start_webui.bat`** file.
3. Your browser will open automatically (at `http://127.0.0.1:5000`).
4. You can drag and drop your CV and job ads, enter your details, and start the bot with a single click!

*(If you prefer to use the bot the classic way via the terminal, follow the instructions below:)*

### 1️⃣ Requirements
*   **Python 3.11** is installed ✅

### 2️⃣ Install Required Packages (or use One-Click-Setup)
Run the `setup_bewerbungsbot.py` script in your PowerShell/CMD:
```bash
python setup_bewerbungsbot.py
```
*(Alternatively: `py setup_bewerbungsbot.py`)*

The `setup_bewerbungsbot.py` makes setup a breeze ("One-Click-Setup"):
*   Asks you step-by-step for your data.
*   Creates the required folder structure, `.env` file, Excel file, and log file.
*   Checks if all libraries are installed and installs missing ones automatically.
*   Makes the bot ready to start and can optionally launch it immediately.

If you prefer to install everything **manually**, open PowerShell or CMD and enter:
```bash
pip install pandas beautifulsoup4 chardet python-dotenv colorama openpyxl
```

### 3️⃣ Collect Job Offers
Go to a job portal such as [AMS Jobroom](https://jobroom.ams.or.at/jobsuche/FreieSuche.jsp).
Go through the job postings. For every offer that has an email address and that you like, save the page by **Right-click > Save as...** into the `Bewerbungsbot/anzeigen` folder (as an HTML file).
If you save, for example, 100 ads and then start the bot, it will extract all email addresses and send an application with your CV/certificates etc. to all of them.

### 4️⃣ Create Folder Structure (Created automatically by setup)
Example of how it should look:
```text
C:\Users\User\Documents\Bewerbungsbot\
│
├── Bewerbungsbot_Template.py
├── setup_bewerbungsbot.py
├── .env
├── lebenslauf.pdf
├── anzeigen\                  <-- Put your saved HTML job ads here
└── Bewerbungen.xlsx
```

### 5️⃣ Create .env File (Created automatically by setup)
Create a file named `.env` in your main folder with the following content:
```env
EMAIL_USER=your.email@gmail.com
EMAIL_PASS=yourAppPassword
SEND_REAL_EMAILS=True
```
> **Tip:** For Gmail, you need an App Password (not your normal password!). [Create one here](https://myaccount.google.com/apppasswords).
> If you only want to test the bot (without sending emails), set this in your `.env`:
> `SEND_REAL_EMAILS=False`

### 6️⃣ Customization
Replace in the code (`Bewerbungsbot_Template.py`):
*   `*NAME*` → with your name
*   `*ORDNER_HTML*`, `*EXCEL_FILE*`, `*CV_FILE*`, `*ENV_PATH*` → with your own file paths

### 7️⃣ Start the Bot
Once everything is set up, start the bot with:
```bash
python Bewerbungsbot_Template.py
```

### 📞 Contact & Support
If you have any problems, feel free to contact me via WhatsApp or Telegram: **+4367762127550** (Regards, Pierre).
For more questions, I am also available in the WhatsApp group: [Join WhatsApp Group](https://chat.whatsapp.com/EHw5Ahb4cUDDIEWZfiyI6x).
Now have fun and many good wishes for success! 😉
