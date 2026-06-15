# Forensic AI Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Server-black?logo=flask)](https://flask.palletsprojects.com/)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?logo=qt)](https://doc.qt.io/qtforpython/)
[![Status: Operational](https://img.shields.io/badge/Status-Fully%20Operational-brightgreen)](#)

> An integrated AI-powered forensic analysis platform. Combines APK security analysis, web scraping, Android emulator integration, voice commands, and real-time monitoring in a unified Flask web dashboard and PyQt5 GUI.

---

## Features

### Forensic Analysis
- **APK Analysis**: Upload Android APKs for automated security assessment via APKTool and MobSF
- **Permission Analysis**: AI-powered risk scoring for mobile application permissions
- **Web Scraping**: Automated data gathering via integrated Scrapy engine
- **Android Emulator**: Real-time stream endpoints for remote Android device control

### Interface Options
- **Web Dashboard**: Flask-based web UI accessible at `localhost:12000`
- **Desktop GUI**: PyQt5 standalone application (`gui_app.py`)
- **REST API**: 8 primary API endpoints for programmatic access

### Voice & AI
- **Voice Control**: Natural language command processing ("run security scan", "analyze apk")
- **Speech Recognition**: SpeechRecognition + pyttsx3 for voice I/O
- **AI Risk Assessment**: Automated risk classification for scanned artifacts

### Monitoring
- **Log Feed**: Centralized real-time activity log stream
- **System Health**: Component status monitoring
- **SQLite Storage**: Local database for scan results and history

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/voice-command` | Process voice/text commands |
| `POST` | `/scrape-website` | Execute web scraping tasks |
| `POST` | `/analyze-apk` | Trigger APK forensic analysis |
| `POST` | `/summarize-permissions` | Generate AI risk report |
| `GET` | `/start-emulator` | Start Android emulator stream |
| `GET` | `/log-feed` | Access real-time activity logs |

---

## Tech Stack

| Component | Technology |
|---|---|
| Web Server | Flask (Werkzeug) |
| Desktop GUI | PyQt5 |
| APK Analysis | APKTool, MobSF |
| Web Scraping | Scrapy |
| Voice AI | SpeechRecognition, pyttsx3 |
| Database | SQLite |
| AI Risk Engine | Custom ML models |

---

## Quick Start

### Prerequisites
- Python 3.10+
- APKTool installed (for APK analysis)
- MobSF (optional, for advanced analysis)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hakunaTgl/forensic-tool.git
cd forensic-tool

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the web server
python app.py
# Web dashboard at http://localhost:12000

# OR run the desktop GUI
python gui_app.py
```

---

## Project Structure

```
forensic-tool/
|-- app.py                  # Flask web server entry point
|-- gui_app.py              # PyQt5 desktop GUI entry point
|-- models/                 # Data models and DB schemas
|-- templates/              # HTML templates for web dashboard
|-- utils/                  # Helper scripts and forensic logic
|-- db.sqlite               # Local SQLite database
|-- SYSTEM_STATUS_REPORT.md # System status and test results
`-- screenshot.png          # UI preview
```

---

## System Status

See [SYSTEM_STATUS_REPORT.md](SYSTEM_STATUS_REPORT.md) for detailed component status and test results.

**Current Status: FULLY OPERATIONAL** (as of 2025-07-10)

---

## License

This project is licensed under the **MIT License**.

---

<p align="center">Built by <a href="https://github.com/hakunaTgl">hakunaTgl (Tylor Fenwick)</a> - <a href="https://hakunatgl.github.io">Portfolio</a></p>
