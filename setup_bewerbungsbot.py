#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, subprocess, sys
from pathlib import Path

# ---------------------------------------------------------------
# BENÖTIGTE MODULE
# ---------------------------------------------------------------
# Installationsname : Importname
REQUIRED_PACKAGES = {
    "pandas": "pandas",
    "beautifulsoup4": "bs4",
    "chardet": "chardet",
    "python-dotenv": "dotenv",
    "colorama": "colorama",
    "openpyxl": "openpyxl"
}

def install_packages():
    print("\n📦 Prüfe und installiere fehlende Python-Pakete ...")
    for pkg_install, pkg_import in REQUIRED_PACKAGES.items():
        try:
            __import__(pkg_import)
            print(f"✅ {pkg_install} bereits installiert")
        except ImportError:
            print(f"⬇️ Installiere {pkg_install} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_install])

def ask(prompt, default=None):
    val = input(f"{prompt} " + (f"[{default}] " if default else "")).strip()
    return val if val else default

def main():
    print("="*60)
    print("🧰 Bewerbungsbot – Automatisches Setup")
    print("="*60)

    # 1. Pfad festlegen
    base_dir = ask("➡️ Installationspfad wählen:", str(Path.home() / "Documents" / "Bewerbungsbot"))
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)

    # 2. Struktur anlegen
    (base / "anzeigen").mkdir(exist_ok=True)
    env_file = base / ".env"
    template_path = base / "Bewerbungsbot_Template.py"

    print(f"\n📁 Projektordner: {base}")

    # 3. Nutzerdaten abfragen
    name = ask("👤 Dein vollständiger Name (für E-Mail Signatur):", "Max Mustermann")
    email = ask("📧 Deine Gmail-Adresse:")
    pw = ask("🔑 Gmail App-Passwort (16-stellig):")
    send_real = ask("💡 Echte Mails senden? (True/False):", "False")

    # 4. .env erstellen (inklusive MEIN_NAME)
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"EMAIL_USER={email}\n")
        f.write(f"EMAIL_PASS={pw}\n")
        f.write(f"SEND_REAL_EMAILS={send_real}\n")
        f.write(f"MEIN_NAME={name}\n") # Wichtig für den Bot!

    print(f"✅ .env Datei erstellt unter: {env_file}")

    # 5. Excel initialisieren (pandas Import erst nach Prüfung)
    install_packages()
    import pandas as pd
    excel_file = base / "Bewerbungen.xlsx"
    if not excel_file.exists():
        df = pd.DataFrame(columns=["Datum", "Firma", "Titel", "Email", "Status"])
        df.to_excel(excel_file, index=False)
        print(f"✅ Excel-Datenbank erstellt: {excel_file}")

    # 6. Template Check
    if not template_path.exists():
        print(Fore.YELLOW + f"\n⚠️ WICHTIG: Kopiere jetzt 'Bewerbungsbot_Template.py' in den Ordner: {base}")
    
    # 7. Start-Option
    start_now = ask("\n▶️ Bewerbungsbot jetzt starten? (ja/nein)", "nein").lower()
    if start_now == "ja":
        if template_path.exists():
            # Wechselt in den Ordner, damit der Bot seine Dateien findet
            os.chdir(base)
            subprocess.run([sys.executable, "Bewerbungsbot_Template.py"])
        else:
            print("❌ Start nicht möglich: Bewerbungsbot_Template.py fehlt im Ordner.")

    print("\n🚀 Setup fertig!")

if __name__ == "__main__":
    main()