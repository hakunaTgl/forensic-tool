"""Forensic Tool - Main Package.

A comprehensive forensic analysis platform for mobile application
security assessment.
"""

__version__ = "1.0.0"
__author__ = "Forensic Tool Contributors"

from . import core
from . import utils

__all__ = ["core", "utils", "__version__"]
