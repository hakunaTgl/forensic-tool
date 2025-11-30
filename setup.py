"""Setup script for Forensic AI Tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="forensic-tool",
    version="1.0.0",
    author="Forensic Tool Contributors",
    author_email="",
    description="A comprehensive forensic analysis platform for mobile application security assessment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hakunaTgl/forensic-tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Flask>=3.0.0",
        "Werkzeug>=3.0.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "numpy>=1.26.0",
        "joblib>=1.3.0",
    ],
    extras_require={
        "gui": ["PyQt5>=5.15.0"],
        "voice": ["SpeechRecognition>=3.10.0", "pyttsx3>=2.90"],
        "scraping": ["Scrapy>=2.11.0"],
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
        "all": [
            "PyQt5>=5.15.0",
            "SpeechRecognition>=3.10.0",
            "pyttsx3>=2.90",
            "Scrapy>=2.11.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "forensic-web=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html"],
    },
)
