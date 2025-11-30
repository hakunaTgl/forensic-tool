import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QTextEdit, QComboBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import gettext
import speech_recognition as sr
import pyttsx3

# Initialize voice
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Language translations
gettext.install('forensic_ai', localedir='locales')
_ = gettext.gettext  # Ensure _ is defined for translations

class ForensicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.theme = 'light'

    def init_ui(self):
        self.setWindowTitle(_('Forensic AI Dashboard'))
        self.setGeometry(200, 200, 600, 500)

        self.status_label = QLabel(_('System Status:'))
        self.logs_output = QTextEdit()
        self.logs_output.setReadOnly(True)

        self.scan_button = QPushButton(_('Check Status'))
        self.scan_button.clicked.connect(self.run_scan)

        self.voice_button = QPushButton(_('🎤 Voice Command'))
        self.voice_button.clicked.connect(self.voice_command)

        self.lang_dropdown = QComboBox()
        self.lang_dropdown.addItems(['en', 'es', 'fr'])
        self.lang_dropdown.currentTextChanged.connect(self.set_language)

        self.theme_button = QPushButton(_('🌓 Toggle Theme'))
        self.theme_button.clicked.connect(self.toggle_theme)

        hbox = QHBoxLayout()
        hbox.addWidget(self.scan_button)
        hbox.addWidget(self.voice_button)
        hbox.addWidget(self.lang_dropdown)
        hbox.addWidget(self.theme_button)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addLayout(hbox)
        layout.addWidget(self.logs_output)

        self.setLayout(layout)

    def run_scan(self):
        try:
            res = requests.get('http://127.0.0.1:5000/status')
            self.logs_output.setPlainText(res.text)
        except Exception as e:
            self.logs_output.setPlainText(_('Error connecting to backend: ') + str(e))

    def set_language(self, lang):
        gettext.translation('forensic_ai', localedir='locales', languages=[lang]).install()
        self.status_label.setText(_('System Status:'))
        self.scan_button.setText(_('Check Status'))
        self.voice_button.setText(_('🎤 Voice Command'))
        self.theme_button.setText(_('🌓 Toggle Theme'))
        self.setWindowTitle(_('Forensic AI Dashboard'))

    def toggle_theme(self):
        palette = QPalette()
        if self.theme == 'light':
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            self.theme = 'dark'
        else:
            palette = QApplication.palette()
            self.theme = 'light'
        QApplication.setPalette(palette)

    def voice_command(self):
        with sr.Microphone() as source:
            self.logs_output.setPlainText(_('Listening for command...'))
            try:
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio)
                self.logs_output.append(_('You said: ') + query)
                if 'status' in query.lower():
                    self.run_scan()
                else:
                    engine.say(_('Sorry, I didn’t understand.'))
                    engine.runAndWait()
            except Exception as e:
                self.logs_output.setPlainText(_('Voice command failed: ') + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ForensicGUI()
    gui.show()
    sys.exit(app.exec_())