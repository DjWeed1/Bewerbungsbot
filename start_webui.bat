@echo off
echo ==========================================
echo Bewerbungsbot Web-UI wird gestartet...
echo ==========================================

REM Pruefen ob Python installiert ist
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH!
    echo Bitte installiere Python 3.11 von python.org und setze das Haeckchen bei "Add Python to PATH".
    pause
    exit
)

REM Abhaengigkeiten installieren
echo Installiere/Pruefe notwendige Bibliotheken (Dies kann beim ersten Mal etwas dauern)...
pip install -q flask pandas beautifulsoup4 chardet python-dotenv colorama openpyxl werkzeug

echo.
echo Alles bereit! Der Browser sollte sich gleich oeffnen...
echo Schliesse dieses Fenster, um den Bot zu beenden.
echo.

REM Starte den Webserver
python webui.py
pause
