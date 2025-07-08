from flask import Flask, render_template, request, redirect, jsonify
from utils.apktool_runner import extract_permissions, decompile_apk
from utils.mobsf_client import upload_apk, scan_uploaded, get_scan_report
from utils.webrtc_bridge import start_emulator_stream
from models.permissions_ai import assess_permissions
from utils.smart_api import log_scan
from models.status_check import check_status
from models.logs_export import export_logs
from utils.status_check import get_system_status
from utils.logs_export import export_scan_logs
from utils.ai_helper import summarize_permissions
from utils.scraper_engine import run as run_web_scraper
import pandas as pd
import os
from werkzeug.utils import secure_filename
from voice_ai_agent import voice_bp
import threading

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'apk'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(voice_bp)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    status = check_status()
    util_status = get_system_status()
    return render_template('index.html', status=status, util_status=util_status)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    perms = extract_permissions(filepath)
    risk = assess_permissions(perms.get('permissions', []))
    log_scan(filename, risk, perms.get('permissions', []), pd.Timestamp.now().isoformat())
    summary = summarize_permissions(perms.get('permissions', []))
    return render_template('dashboard.html', filename=filename, risk=risk, permissions=perms.get('permissions', []), summary=summary)

@app.route('/logs')
def logs():
    logs_model = export_logs()
    logs_utils = export_scan_logs()
    return jsonify({"model_logs": logs_model, "utils_logs": logs_utils})

@app.route('/status')
def status():
    return jsonify(check_status())

@app.route('/util-status')
def util_status():
    return jsonify(get_system_status())

@app.route('/summarize-permissions', methods=['POST'])
def summarize():
    permissions = request.json.get('permissions', [])
    summary = summarize_permissions(permissions)
    return jsonify({"summary": summary})

@app.route('/run-scraper')
def run_scraper_route():
    threading.Thread(target=run_web_scraper).start()
    return "Web scraper started! Check output.json for results."

@app.route('/start-emulator')
def start_emulator():
    result = start_emulator_stream()
    return jsonify({"emulator_started": result})

if __name__ == '__main__':
    app.run(debug=True)