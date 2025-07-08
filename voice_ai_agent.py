from flask import Blueprint, render_template, jsonify, request, Flask
import os
import re
import tempfile
from werkzeug.utils import secure_filename
import requests
from typing import Any

voice_bp = Blueprint('voice_bp', __name__)

# Log store tracks status, file links, API calls, and transcripts
log_store: dict[str, Any] = {
    "status": "Idle",
    "file_links": [],
    "api_calls": [],
    "transcripts": []
}

@voice_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@voice_bp.route('/log-feed')
def log_feed():
    return jsonify(log_store)

@voice_bp.route('/scrape-website', methods=['POST'])
def scrape_website():
    log_store["status"] = "Scraping"
    log_store["api_calls"].append("/scrape-website")
    data = request.json
    url = data.get('url')
    file_links = []
    if url:
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            # Find all downloadable file links (expand as needed)
            file_links = re.findall(r'https?://[^\s"\']+\.(apk|zip|exe|dmg|tar\.gz|pdf|docx|xlsx|csv|jpg|png)', resp.text)
            file_links = list(set(file_links))
        except Exception as e:
            log_store["status"] = f"Scraping Error: {e}"
            return jsonify({'error': str(e)}), 500
    log_store["file_links"] = file_links
    log_store["status"] = "Scraping Complete"
    return jsonify({'file_links': file_links, 'status': log_store["status"]})

@voice_bp.route('/voice-command', methods=['POST'])
def process_voice_command():
    data = request.json
    transcript = data.get("transcript")
    log_store["transcripts"].append(transcript)
    log_store["api_calls"].append("/voice-command")
    # Dummy AI response for demonstration
    return jsonify({"response": f"Processed: {transcript}"})

@voice_bp.route('/analyze-apk', methods=['POST'])
def analyze_apk():
    log_store["api_calls"].append("/analyze-apk")
    apk = request.files.get('apk')
    if not apk:
        return jsonify({'error': 'No APK uploaded'}), 400
    temp_dir = tempfile.gettempdir()
    apk_path = os.path.join(temp_dir, secure_filename(apk.filename))
    apk.save(apk_path)
    # Dummy analysis
    analysis = {"apk_path": apk_path, "permissions": ["android.permission.INTERNET"]}
    return jsonify({'analysis': analysis, 'apk_path': apk_path})

@voice_bp.route('/download-and-analyze', methods=['POST'])
def download_and_analyze():
    log_store["api_calls"].append("/download-and-analyze")
    data = request.json
    file_url = data.get('file_url')
    if not file_url:
        return jsonify({'error': 'No file URL provided'}), 400
    # Download file to temp
    temp_dir = tempfile.gettempdir()
    local_filename = secure_filename(file_url.split('/')[-1])
    local_path = os.path.join(temp_dir, local_filename)
    try:
        with requests.get(file_url, stream=True, timeout=20) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        # Dummy analysis
        analysis = {"file_path": local_path, "info": "Downloaded and analyzed"}
        return jsonify({'analysis': analysis, 'local_path': local_path})
    except Exception as e:
        return jsonify({'error': f'Download/analysis failed: {e}'}), 500

# --- App factory and launch ---
def create_app():
    app = Flask(__name__)
    app.register_blueprint(voice_bp)
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB upload limit
    app.static_folder = 'static'
    app.template_folder = 'templates'
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
