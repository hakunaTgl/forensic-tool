# This file makes 'utils' a Python package

from .apktool_runner import extract_permissions, decompile_apk
from .mobsf_client import upload_apk, get_scan_report
from .webrtc_bridge import start_emulator_stream
from .smart_api import log_scan

def extract_permissions(apk_path: str) -> dict[str, str]:
    # implementation

def decompile_apk(apk_path: str, output_dir: str = "decompiled_output") -> dict[str, str]:
    # implementation