#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, time, random, smtplib, chardet
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage
from dotenv import load_dotenv
from colorama import init as colorama_init, Fore

colorama_init(autoreset=True)


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


ENV_PATH = ".env"
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

ORDNER_HTML = get_env("ORDNER_HTML", "./anzeigen")
EXCEL_FILE = get_env("EXCEL_FILE", "Bewerbungen.xlsx")
LOG_FILE = get_env("LOG_FILE", "bewerbungslog.txt")
CV_FILE = safe_find_file("Lebenslauf.pdf", ["lebenslauf", "cv", "resume"])
ZEUGNIS_FILE = safe_find_file("Zeugnisse.pdf", ["zeugnis", "certificate"])

EMAIL_USER = get_env("EMAIL_USER", "DEINE_MAIL@gmail.com")
EMAIL_PASS = get_env("EMAIL_PASS", "DEIN_APP_PASSWORT")
SEND_REAL_EMAILS = get_env("SEND_REAL_EMAILS", "False").lower() in ("1", "true", "yes")
MEIN_NAME = get_env("MEIN_NAME", "Dein Vorname Nachname")

# Explicit safety switch: real sending must be enabled deliberately.
ALLOW_REAL_EMAILS = get_env("ALLOW_REAL_EMAILS", "False").lower() in ("1", "true", "yes")
DELAY_MIN = max(1, int(get_env("DELAY_MIN_SECONDS", "15")))
DELAY_MAX = max(DELAY_MIN, int(get_env("DELAY_MAX_SECONDS", "45")))


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


def extract_all_emails(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    found = re.findall(pattern, text)
    return sorted(set(e.strip(".,; ") for e in found if not e.lower().endswith((".jpg", ".png", ".gif"))))


def extract_job_info(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    title = "Unbekannt"
    for tag in ["h1", "title", "strong"]:
        el = soup.find(tag)
        if el and len(el.text.strip()) > 5:
            title = el.text.strip()
            break

    company = "Unbekanntes Unternehmen"
    for label in ["Firma", "Unternehmen", "Arbeitgeber"]:
        m = re.search(label + r"\s*[:\-]?\s*([A-Za-zÄÖÜäöüß0-9\s\.\-&]+)", text)
        if m:
            company = m.group(1).strip()
            break

    return {"Titel": title, "Firma": company, "Emails": extract_all_emails(html)}


def send_application(to, info):
    subject = f"Bewerbung als {info['Titel']} - {MEIN_NAME}"
    body = (
        f"Sehr geehrte Damen und Herren,\n\n"
        f"mit großem Interesse bewerbe ich mich auf Ihre Stelle als {info['Titel']} "
        f"bei {info['Firma']}.\n\n"
        f"Anbei erhalten Sie meine Bewerbungsunterlagen (Lebenslauf und Zeugnisse).\n\n"
        f"Über die Einladung zu einem persönlichen Gespräch freue ich mich sehr.\n\n"
        f"Mit freundlichen Grüßen,\n{MEIN_NAME}"
    )

    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    if CV_FILE and os.path.exists(CV_FILE):
        with open(CV_FILE, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(CV_FILE))

    if SEND_REAL_EMAILS:
        if not ALLOW_REAL_EMAILS:
            log("Echter E-Mail-Versand ist blockiert: ALLOW_REAL_EMAILS=True muss bewusst gesetzt werden.", "error")
            return False
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
            return True
        except Exception as e:
            log(f"Fehler beim Senden: {e}", "error")
            return False

    log(f"[TESTMODUS] Mail an {to} simuliert.", "warn")
    return True


def main():
    if not EMAIL_USER or "DEINE_MAIL" in EMAIL_USER:
        log("E-Mail Daten nicht konfiguriert!", "error")
        return

    if SEND_REAL_EMAILS and not ALLOW_REAL_EMAILS:
        log("SEND_REAL_EMAILS=True erkannt, aber ALLOW_REAL_EMAILS=False. Kein echter Versand.", "error")
        return

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=["Datum", "Firma", "Titel", "Email", "Status"])

    if "Email" not in df.columns:
        df["Email"] = ""
    known_emails = {str(v).strip().lower() for v in df["Email"].dropna() if str(v).strip()}

    if not os.path.exists(ORDNER_HTML):
        log(f"Ordner {ORDNER_HTML} nicht gefunden!", "error")
        return

    files = [f for f in os.listdir(ORDNER_HTML) if f.lower().endswith(".html")]
    log(f"Starte Durchlauf... {len(files)} Dateien gefunden.", "info")

    for fname in files:
        path = os.path.join(ORDNER_HTML, fname)
        try:
            with open(path, "rb") as f:
                raw = f.read()
                enc = chardet.detect(raw)["encoding"] or "utf-8"
            with open(path, "r", encoding=enc, errors="ignore") as f:
                html = f.read()
        except OSError as e:
            log(f"Datei konnte nicht gelesen werden: {fname}: {e}", "error")
            continue

        info = extract_job_info(html)
        if not info["Emails"]:
            log(f"Keine Email in {fname} gefunden.", "warn")
            continue

        for email in info["Emails"]:
            normalized_email = email.strip().lower()
            if normalized_email in known_emails:
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
                known_emails.add(normalized_email)
                df.to_excel(EXCEL_FILE, index=False)
                log(f"Erfolg: {info['Firma']} kontaktiert.", "success")
                time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    log("Fertig!", "success")


if __name__ == "__main__":
    main()
