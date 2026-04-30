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

### 💡 Ideen & Wunschliste (Future Features)
Das Projekt ist bereits jetzt eine enorme Hilfe, aber es gibt noch einige großartige Ideen, wie wir den Bot in Zukunft erweitern könnten:

* **🤖 1. KI-generierte Anschreiben (Die "Killer-Funktion")**
  Aktuell verschickt der Bot einen Standard-Text. Durch die Anbindung der OpenAI (ChatGPT) API könnte der Bot die hochgeladene Stellenanzeige analysieren und in Sekundenschnelle ein maßgeschneidertes, hochprofessionelles Anschreiben für genau diese Firma generieren!
* **🕸️ 2. Automatisches Suchen (Scraping)**
  Anstatt HTML-Dateien manuell zu speichern, könntest du in Zukunft nur noch *"Suche nach Verkäufer in Wien"* eingeben. Der Bot sucht automatisch auf Job-Portalen, sammelt z.B. 50 Anzeigen und bewirbt sich selbstständig!
* **📊 3. Ein "Bewerbungs-Dashboard" in der Web-UI**
  Eine visuelle Darstellung deiner `Bewerbungen.xlsx` direkt in der Web-Oberfläche. Du hättest ein kleines CRM-System, in dem du auf einen Blick Datum, Firmenname und Jobtitel siehst.
* **📑 4. Mehrere Lebensläufe unterstützen**
  Ein Dropdown-Menü in der Web-UI, mit dem du aus verschiedenen Lebensläufen (z.B. Variante A für Bürokraft, Variante B für Empfang) wählen kannst, bevor der Bot startet.

> [!IMPORTANT]
> **Du möchtest eines dieser Features nutzen?**
> Wenn dir eine dieser Ideen gefällt und du sie in diesem Projekt haben möchtest, melde dich einfach bei mir unter **pierre.fikota@gmail.com** oder in unserer **[WhatsApp-Gruppe](https://chat.whatsapp.com/EHw5Ahb4cUDDIEWZfiyI6x)** und ich werde die Erweiterung erschaffen! 😊

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

### 💡 Ideas & Wishlist (Future Features)
The project is already a huge help, but there are some great ideas on how we could expand the bot in the future:

* **🤖 1. AI-Generated Cover Letters (The "Killer Feature")**
  Currently, the bot sends a standard text. By connecting the OpenAI (ChatGPT) API, the bot could analyze the uploaded job ad and generate a tailor-made, highly professional cover letter for exactly that company in seconds!
* **🕸️ 2. Automated Searching (Scraping)**
  Instead of saving HTML files manually, you could just enter *"Search for sales assistant in Vienna"*. The bot would automatically search job portals, collect e.g. 50 ads, and apply on its own!
* **📊 3. An "Application Dashboard" in the Web UI**
  A visual representation of your `Bewerbungen.xlsx` directly in the web interface. You would have a small CRM system where you can see the date, company name, and job title at a glance.
* **📑 4. Support for Multiple CVs**
  A dropdown menu in the Web UI that lets you choose from different uploaded CVs (e.g. Variant A for office work, Variant B for reception) before the bot starts.

> [!IMPORTANT]
> **Do you want to use one of these features?**
> If you like any of these ideas and want to have them in this project, simply contact me at **pierre.fikota@gmail.com** or in our **[WhatsApp Group](https://chat.whatsapp.com/EHw5Ahb4cUDDIEWZfiyI6x)** and I will build the extension! 😊
