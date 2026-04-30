import os
import subprocess
import threading
import queue
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.utils import secure_form_data, secure_filename
import time

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANZEIGEN_DIR = os.path.join(BASE_DIR, "anzeigen")
ENV_PATH = os.path.join(BASE_DIR, ".env")
CV_PATH = os.path.join(BASE_DIR, "lebenslauf.pdf")

# Ensure directories exist
os.makedirs(ANZEIGEN_DIR, exist_ok=True)

# Queue for bot logs
log_queue = queue.Queue()
bot_process = None

def run_bot():
    global bot_process
    try:
        # Run the bot script
        bot_process = subprocess.Popen(
            ["python", "Bewerbungsbot_Template.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=BASE_DIR
        )
        
        for line in bot_process.stdout:
            log_queue.put(line)
            
        bot_process.wait()
        log_queue.put(f"\n[System] Bot beendet mit Code {bot_process.returncode}\n")
    except Exception as e:
        log_queue.put(f"\n[Fehler] Konnte Bot nicht starten: {str(e)}\n")
    finally:
        bot_process = None

@app.route('/')
def index():
    # Read current .env variables if they exist
    env_data = {"EMAIL_USER": "", "EMAIL_PASS": "", "SEND_REAL_EMAILS": "False"}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    if key in env_data:
                        env_data[key] = val
                        
    return render_template("index.html", env_data=env_data)

@app.route('/api/save_config', methods=['POST'])
def save_config():
    data = request.json
    try:
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write(f"EMAIL_USER={data.get('email', '')}\n")
            f.write(f"EMAIL_PASS={data.get('password', '')}\n")
            f.write(f"SEND_REAL_EMAILS={data.get('send_real', 'False')}\n")
        return jsonify({"status": "success", "message": "Konfiguration gespeichert!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/upload_cv', methods=['POST'])
def upload_cv():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Keine Datei hochgeladen"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Keine Datei ausgewählt"}), 400
    
    if file and file.filename.endswith('.pdf'):
        file.save(CV_PATH)
        return jsonify({"status": "success", "message": "Lebenslauf erfolgreich hochgeladen!"})
    return jsonify({"status": "error", "message": "Nur PDF-Dateien sind erlaubt."}), 400

@app.route('/api/upload_anzeigen', methods=['POST'])
def upload_anzeigen():
    if 'files[]' not in request.files:
        return jsonify({"status": "error", "message": "Keine Dateien hochgeladen"}), 400
    
    files = request.files.getlist('files[]')
    saved_count = 0
    for file in files:
        if file and (file.filename.endswith('.html') or file.filename.endswith('.htm')):
            filename = secure_filename(file.filename)
            file.save(os.path.join(ANZEIGEN_DIR, filename))
            saved_count += 1
            
    return jsonify({"status": "success", "message": f"{saved_count} Anzeigen hochgeladen!"})

@app.route('/api/clear_anzeigen', methods=['POST'])
def clear_anzeigen():
    try:
        for filename in os.listdir(ANZEIGEN_DIR):
            file_path = os.path.join(ANZEIGEN_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({"status": "success", "message": "Alle Anzeigen gelöscht!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    global bot_process
    if bot_process is not None:
        return jsonify({"status": "error", "message": "Bot läuft bereits!"}), 400
    
    # Clear old logs
    while not log_queue.empty():
        try:
            log_queue.get_nowait()
        except queue.Empty:
            break
            
    thread = threading.Thread(target=run_bot)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "success", "message": "Bot gestartet!"})

@app.route('/api/stream_logs')
def stream_logs():
    def generate():
        while True:
            try:
                # Wait for new log line
                line = log_queue.get(timeout=1.0)
                yield f"data: {line}\n\n"
            except queue.Empty:
                if bot_process is None and log_queue.empty():
                    # Bot finished and queue empty
                    yield "event: end\ndata: \n\n"
                    break
                else:
                    # Keep connection alive
                    yield ": keepalive\n\n"
            
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    import webbrowser
    from threading import Timer
    
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000")
        
    Timer(1.5, open_browser).start()
    print("Starte lokale Web-UI für Bewerbungsbot...")
    app.run(host='127.0.0.1', port=5000, debug=False)
