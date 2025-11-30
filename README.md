# Forensic AI Tool

A comprehensive forensic analysis platform for mobile application security assessment, featuring APK analysis, permission risk assessment, web scraping capabilities, and an AI-powered assistant interface.

## 🎯 Project Overview

The Forensic AI Tool is designed to help security researchers and analysts perform in-depth analysis of Android applications. It provides:

- **APK Analysis**: Extract and analyze permissions from Android applications
- **Permission Risk Assessment**: AI-powered risk scoring for application permissions
- **Web Scraping**: Automated discovery of downloadable files from websites
- **Voice Commands**: Voice-activated interface for hands-free operation
- **Emulator Integration**: Stream and interact with Android emulators
- **Comprehensive Logging**: Track all analysis activities and results

## 📁 Repository Structure

```
forensic-tool/
├── src/
│   ├── core/                    # Core forensic functionality
│   │   ├── permissions_ai.py    # Permission risk assessment
│   │   ├── status_check.py      # System status monitoring
│   │   └── logs_export.py       # Log export functionality
│   └── utils/                   # Utility modules
│       ├── apktool_runner.py    # APK decompilation tools
│       ├── mobsf_client.py      # Mobile Security Framework client
│       ├── webrtc_bridge.py     # Emulator streaming
│       ├── smart_api.py         # Database operations
│       ├── ai_helper.py         # AI assistance utilities
│       ├── scraper_engine.py    # Web scraping engine
│       ├── status_check.py      # Utility status checks
│       └── logs_export.py       # Scan log exports
├── tests/                       # Test cases
│   └── test_core.py             # Core functionality tests
├── templates/                   # HTML templates for web interface
│   ├── index.html               # Main dashboard
│   ├── dashboard.html           # Analysis dashboard
│   └── ...
├── docs/                        # Additional documentation
│   └── API.md                   # API documentation
├── app.py                       # Main Flask application
├── gui_app.py                   # PyQt5 GUI application
├── voice_ai_agent.py            # Voice command processor
├── setup.py                     # Installation script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Optional: APKTool for APK decompilation
- Optional: Android SDK for emulator features

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/hakunaTgl/forensic-tool.git
   cd forensic-tool
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package** (optional, for development)
   ```bash
   pip install -e .
   ```

5. **Run the application**
   ```bash
   # Web interface
   python app.py

   # GUI interface (requires display)
   python gui_app.py
   ```

6. **Access the web interface**
   Open your browser and navigate to `http://localhost:12000`

### Optional Dependencies

For full functionality, install these external tools:

- **APKTool**: For APK decompilation
  ```bash
  # Ubuntu/Debian
  sudo apt install apktool

  # macOS
  brew install apktool
  ```

- **MobSF**: For advanced mobile security analysis
  - Follow instructions at [MobSF GitHub](https://github.com/MobSF/Mobile-Security-Framework-MobSF)

## 📖 Usage Guide

### Web Interface

The web interface provides access to all forensic features:

1. **AI Chat**: Interact with the forensic AI assistant
   - Type commands or use voice input
   - Get help with analysis tasks

2. **APK Analysis**: Upload and analyze Android applications
   - Upload APK files via drag-and-drop or file selector
   - View extracted permissions and risk assessment

3. **Website Scraper**: Discover downloadable files
   - Enter a URL to scan for downloadable files
   - Click on discovered files to download and analyze

4. **Logs**: View analysis history
   - Track all performed scans
   - Export logs for reporting

5. **Emulator**: Control Android emulator streams
   - Start/stop emulator sessions
   - View emulator output

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/status` | GET | System health check |
| `/util-status` | GET | Utility status |
| `/upload` | POST | Upload APK for analysis |
| `/voice-command` | POST | Process voice commands |
| `/scrape-website` | POST | Scrape website for files |
| `/analyze-apk` | POST | Analyze uploaded APK |
| `/summarize-permissions` | POST | Get permission summary |
| `/start-emulator` | GET | Start emulator stream |
| `/logs` | GET | Get scan logs |
| `/log-feed` | GET | Get live log feed |

### Example API Usage

```python
import requests

# Check system status
response = requests.get('http://localhost:12000/status')
print(response.json())

# Analyze permissions
permissions = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.CAMERA"
]
response = requests.post(
    'http://localhost:12000/summarize-permissions',
    json={'permissions': permissions}
)
print(response.json())

# Scrape website for files
response = requests.post(
    'http://localhost:12000/scrape-website',
    json={'url': 'https://example.com'}
)
print(response.json())
```

### GUI Application

The GUI application provides a desktop interface:

```bash
python gui_app.py
```

Features:
- System status monitoring
- Voice command input
- Theme switching (light/dark)
- Multi-language support (en, es, fr)

### Command Line Testing

Run the system tests:

```bash
# Start the server first
python app.py &

# Run tests
python system_test.py
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MOBSF_API_KEY` | MobSF API authentication key | `your-key-here` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `FLASK_HOST` | Server host | `0.0.0.0` |
| `FLASK_PORT` | Server port | `12000` |

### Database

The application uses SQLite for storing scan logs. The database is automatically created at `db.sqlite` in the project root.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src

# Run specific test file
python -m pytest tests/test_core.py
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes: `git commit -m "Add your feature"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed

## 📋 Credits

### Contributors

- Project Maintainers and Contributors

### Technologies Used

- **Flask**: Web framework for the API and web interface
- **PyQt5**: Desktop GUI framework
- **Scrapy**: Web scraping framework
- **SQLite**: Database for logging
- **Werkzeug**: WSGI utilities
- **requests**: HTTP library
- **pandas**: Data manipulation
- **speech_recognition**: Voice input processing
- **pyttsx3**: Text-to-speech

### Resources

- Android Permission Documentation
- Mobile Security Framework (MobSF)
- APKTool Project

## 📄 License

This project is available for use under standard open-source terms. Please review the LICENSE file for specific terms and conditions.

## 🔒 Security

### Reporting Security Issues

If you discover a security vulnerability, please:
1. Do not open a public issue
2. Contact the maintainers directly
3. Provide detailed information about the vulnerability

### Best Practices

- Always run the tool in a controlled environment
- Be cautious when analyzing unknown APK files
- Keep dependencies updated for security patches

## 📞 Support

- Open an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Provide detailed reproduction steps for bugs

---

**Note**: This tool is intended for legitimate security research and analysis purposes only. Always obtain proper authorization before analyzing applications you do not own.
