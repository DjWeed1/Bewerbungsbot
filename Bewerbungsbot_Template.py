#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, time, random, smtplib, chardet
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from colorama import init as colorama_init, Fore

colorama_init(autoreset=True)

# -------------------------------------------------------------------
# HILFSFUNKTIONEN / HELPER FUNCTIONS
# -------------------------------------------------------------------
def get_env(key, default=None, required=False):
    val = os.getenv(key, default)
    if required and (val is None or val == ""):
        return None
    return val

def safe_find_file(default_name, keywords, folder="."):
    try:
        for f in os.listdir(folder):
            name = f.lower()
            if any(k in name for k in keywords) and name.endswith((".pdf", ".jpg", ".png")):
                return os.path.join(folder, f)
    except Exception:
        pass
    return os.path.join(folder, default_name) if os.path.exists(os.path.join(folder, default_name)) else None

# -------------------------------------------------------------------
# CONFIG & PFADE / CONFIG & PATHS
# -------------------------------------------------------------------
ENV_PATH = ".env" # HIER: Pfad zur .env Datei prüfen | HERE: Check path to .env file
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

# Falls keine .env genutzt wird, hier die Pfade direkt anpassen:
# If no .env is used, adjust the paths directly here:
ORDNER_HTML = get_env("ORDNER_HTML", "./anzeigen") # HIER: Ordner mit HTML-Anzeigen | HERE: Folder with HTML ads
EXCEL_FILE  = get_env("EXCEL_FILE", "Bewerbungen.xlsx") # HIER: Name der Excel-Logdatei | HERE: Name of Excel log file
LOG_FILE    = "bewerbungslog.txt" # HIER: Name der Text-Logdatei | HERE: Name of text log file

# Dateisuche für Anhänge (Keywords anpassen, falls nötig)
# File search for attachments (adjust keywords if necessary)
CV_FILE      = safe_find_file("Lebenslauf.pdf", ["lebenslauf", "cv", "resume"]) # HIER: Name deines CVs | HERE: Name of your CV
ZEUGNIS_FILE = safe_find_file("Zeugnisse.pdf", ["zeugnis", "certificate"]) # HIER: Name der Zeugnisse | HERE: Name of certificates

# E-Mail Account Daten (Müssen in der .env oder hier stehen)
# E-mail account data (Must be in .env or here)
EMAIL_USER       = get_env("EMAIL_USER", "DEINE_MAIL@gmail.com") # HIER: Deine E-Mail Adresse | HERE: Your email address
EMAIL_PASS       = get_env("EMAIL_PASS", "DEIN_APP_PASSWORT") # HIER: Google App-Passwort (16-stellig) | HERE: Google App Password (16 digits)
SEND_REAL_EMAILS = get_env("SEND_REAL_EMAILS", "False").lower() in ("1", "true", "yes") # HIER: True zum Senden, False für Test | HERE: True to send, False for test
MEIN_NAME        = get_env("MEIN_NAME", "Dein Vorname Nachname") # HIER: Dein voller Name für die Signatur | HERE: Your full name for signature

# -------------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------------
def log(text, level="info"):
    colors = {"info": Fore.CYAN, "success": Fore.GREEN, "warn": Fore.YELLOW, "error": Fore.RED}
    color = colors.get(level, Fore.WHITE)
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {text}"
    print(color + line)
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

# -------------------------------------------------------------------
# ANALYSE-LOGIK / ANALYSIS LOGIC
# -------------------------------------------------------------------
def extract_all_emails(text):
    # Regex für E-Mail Adressen (meist keine Änderung nötig)
    # Regex for email addresses (usually no change needed)
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    found = re.findall(pattern, text)
    return sorted(set(e.strip(".,; ") for e in found if not e.lower().endswith((".jpg", ".png", ".gif"))))

def extract_job_info(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Titel Suche (Falls die Seitenstruktur anders ist, Tags anpassen)
    # Title search (If page structure is different, adjust tags)
    title = "Unbekannt"
    for tag in ["h1", "title", "strong"]: # HIER: Tags für Jobtitel (h1, h2, etc.) | HERE: Tags for job title
        el = soup.find(tag)
        if el and len(el.text.strip()) > 5:
            title = el.text.strip()
            break

    # Firma Suche (Keywords für die Firma anpassen)
    # Company search (Adjust keywords for company)
    company = "Unbekanntes Unternehmen"
    for label in ["Firma", "Unternehmen", "Arbeitgeber"]: # HIER: Signalwörter für Firmenname | HERE: Keywords for company name
        m = re.search(label + r"\s*[:\-]?\s*([A-Za-zÄÖÜäöüß0-9\s\.\-&]+)", text)
        if m:
            company = m.group(1).strip()
            break

    return {
        "Titel": title,
        "Firma": company,
        "Emails": extract_all_emails(html)
    }

# -------------------------------------------------------------------
# BEWERBUNGSTEXT / APPLICATION TEXT
# -------------------------------------------------------------------
def send_application(to, info):
    # Betreffzeile anpassen | Adjust subject line
    subject = f"Bewerbung als {info['Titel']} - {MEIN_NAME}" # HIER: Betreff-Format | HERE: Subject format
    
    # Der eigentliche Text der E-Mail | The actual body of the email
    body = (
        f"Sehr geehrte Damen und Herren,\n\n" # HIER: Anrede | HERE: Salutation
        f"mit großem Interesse bewerbe ich mich auf Ihre Stelle als {info['Titel']} " # HIER: Einleitung | HERE: Intro
        f"bei {info['Firma']}.\n\n"
        f"Anbei erhalten Sie meine Bewerbungsunterlagen (Lebenslauf und Zeugnisse).\n\n" # HIER: Hinweis auf Anhänge | HERE: Mention attachments
        f"Über die Einladung zu einem persönlichen Gespräch freue ich mich sehr.\n\n"
        f"Mit freundlichen Grüßen,\n{MEIN_NAME}" # HIER: Grußformel | HERE: Closing
    )

    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    # Anhänge hinzufügen | Adding attachments
    if CV_FILE and os.path.exists(CV_FILE):
        with open(CV_FILE, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", 
                               filename=os.path.basename(CV_FILE))

    if SEND_REAL_EMAILS:
        try:
            # SMTP Server Daten (Hier für Gmail, sonst anpassen)
            # SMTP server data (Here for Gmail, otherwise adjust)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: # HIER: SMTP Server & Port | HERE: SMTP server & port
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
            return True
        except Exception as e:
            log(f"Fehler beim Senden: {e}", "error")
            return False
    else:
        log(f"[TESTMODUS] Mail an {to} simuliert.", "warn")
        return True

# -------------------------------------------------------------------
# HAUPTPROGRAMM / MAIN RUNNER
# -------------------------------------------------------------------
def main():
    if not EMAIL_USER or "DEINE_MAIL" in EMAIL_USER:
        log("E-Mail Daten nicht konfiguriert!", "error") # HIER: Fehlermeldung prüfen | HERE: Check error message
        return

    # Excel-Datenbank Setup
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        # Spaltennamen der Excel-Datei | Column names of excel file
        df = pd.DataFrame(columns=["Datum", "Firma", "Titel", "Email", "Status"])

    if not os.path.exists(ORDNER_HTML):
        log(f"Ordner {ORDNER_HTML} nicht gefunden!", "error")
        return

    files = [f for f in os.listdir(ORDNER_HTML) if f.endswith(".html")]
    log(f"Starte Durchlauf... {len(files)} Dateien gefunden.", "info")

    for fname in files:
        path = os.path.join(ORDNER_HTML, fname)
        with open(path, "rb") as f:
            raw = f.read()
            enc = chardet.detect(raw)["encoding"] or "utf-8"
        
        with open(path, "r", encoding=enc, errors="ignore") as f:
            html = f.read()

        info = extract_job_info(html)
        
        if not info["Emails"]:
            log(f"Keine Email in {fname} gefunden.", "warn")
            continue

        for email in info["Emails"]:
            # Dubletten-Schutz (Verhindert doppelte E-Mails)
            # Duplicate protection (Prevents sending twice)
            if email in df["Email"].values:
                log(f"Überspringe (bereits kontaktiert): {email}", "info")
                continue

            success = send_application(email, info)
            
            if success:
                new_row = {
                    "Datum": datetime.now().strftime("%d.%m.%Y"),
                    "Firma": info["Firma"],
                    "Titel": info["Titel"],
                    "Email": email,
                    "Status": "Gesendet" if SEND_REAL_EMAILS else "Test"
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                log(f"Erfolg: {info['Firma']} kontaktiert.", "success")
                
                # Wartezeit zwischen Mails (Gegen Spam-Filter)
                # Wait time between emails (Anti-spam measure)
                time.sleep(random.uniform(10, 30)) # HIER: Sekunden Pause (Min, Max) | HERE: Seconds delay (Min, Max)

    log("Fertig!", "success")

if __name__ == "__main__":
    main()