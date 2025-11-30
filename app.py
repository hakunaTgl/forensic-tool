"""Main Flask application for Forensic AI Tool.

This module provides the web interface and API endpoints for the
forensic analysis platform.
"""

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
import logging
from werkzeug.utils import secure_filename
from voice_ai_agent import voice_bp
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'apk'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.register_blueprint(voice_bp)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed.
    
    Args:
        filename: Name of the file to check.
        
    Returns:
        bool: True if file extension is allowed.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({"error": "File too large. Maximum size is 100MB."}), 413


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server error."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error. Please try again later."}), 500


@app.route('/')
def index():
    """Render the main dashboard."""
    try:
        status = check_status()
        util_status = get_system_status()
        return render_template('index.html', status=status, util_status=util_status)
    except Exception as e:
        logger.error(f"Error loading index: {e}")
        return jsonify({"error": "Failed to load dashboard"}), 500

@app.route('/upload', methods=['POST'])
def upload():
    """Handle APK file upload and analysis."""
    try:
        if 'file' not in request.files:
            logger.warning("Upload attempted without file")
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only APK files are allowed."}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"Processing uploaded file: {filename}")
        
        perms = extract_permissions(filepath)
        permissions_list = perms.get('permissions', [])
        
        # Handle string permissions (comma-separated)
        if isinstance(permissions_list, str):
            permissions_list = [p.strip() for p in permissions_list.split(',')]
        
        risk = assess_permissions(permissions_list)
        log_scan(filename, risk, permissions_list, pd.Timestamp.now().isoformat())
        summary = summarize_permissions(permissions_list)
        
        return render_template(
            'dashboard.html',
            filename=filename,
            risk=risk,
            permissions=permissions_list,
            summary=summary
        )
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

@app.route('/logs')
def logs():
    """Get all scan logs."""
    try:
        logs_model = export_logs()
        logs_utils = export_scan_logs()
        return jsonify({"model_logs": logs_model, "utils_logs": logs_utils})
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        return jsonify({"error": "Failed to retrieve logs", "model_logs": [], "utils_logs": []})


@app.route('/status')
def status():
    """Get system status."""
    try:
        return jsonify(check_status())
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route('/util-status')
def util_status():
    """Get utility status."""
    try:
        return jsonify(get_system_status())
    except Exception as e:
        logger.error(f"Util status error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/summarize-permissions', methods=['POST'])
def summarize():
    """Summarize Android permissions."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        permissions = data.get('permissions', [])
        summary = summarize_permissions(permissions)
        return jsonify({"summary": summary})
    except Exception as e:
        logger.error(f"Summarize error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/run-scraper')
def run_scraper_route():
    """Start the web scraper in background."""
    try:
        threading.Thread(target=run_web_scraper, daemon=True).start()
        return jsonify({
            "message": "Web scraper started!",
            "output_file": "output.json"
        })
    except Exception as e:
        logger.error(f"Scraper error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/start-emulator')
def start_emulator():
    """Start the Android emulator stream."""
    try:
        result = start_emulator_stream()
        return jsonify({"emulator_started": result})
    except Exception as e:
        logger.error(f"Emulator error: {e}")
        return jsonify({"emulator_started": False, "error": str(e)})

def main():
    """Run the Flask application."""
    logger.info("Starting Forensic AI Tool server...")
    # Debug mode is controlled by environment variable (defaults to False for security)
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', '12000'))
    app.run(debug=debug_mode, host=host, port=port)


if __name__ == '__main__':
    main()