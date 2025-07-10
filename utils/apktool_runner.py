# apktool_runner.py
import subprocess
import os
import logging
from typing import Dict

def run_aapt(apk_path):
    try:
        output = subprocess.check_output(['aapt', 'dump', 'permissions', apk_path])
        return output.decode()
    except Exception as e:
        return f"AAPT failed: {e}"

def run_apktool(apk_path, output_dir=None):
    if not output_dir:
        output_dir = apk_path.replace('.apk', '_decoded')
    try:
        subprocess.run(['apktool', 'd', apk_path, '-o', output_dir, '-f'], check=True)
        return output_dir
    except Exception as e:
        return f"APKTool failed: {e}"

def extract_permissions(apk_path: str) -> Dict[str, str]:
    # Dummy implementation for demonstration
    # Replace with real APK analysis logic
    return {
        "apk_path": apk_path,
        "permissions": "android.permission.INTERNET, android.permission.ACCESS_FINE_LOCATION"
    }

def decompile_apk(apk_path: str, output_dir: str = "decompiled_output") -> dict[str, str]:
    """
    Decompiles an APK using apktool.
    Returns a dict with status and output path, or error message.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(['apktool', 'd', apk_path, '-f', '-o', output_dir], check=True)
        return {"status": "success", "path": output_dir}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_apk(apk_path):
    aapt_data = run_aapt(apk_path)
    decoded_dir = run_apktool(apk_path)
    return {
        "permissions": aapt_data,
        "decoded_directory": decoded_dir
    }

def extract_apk_info(apk_path):
    try:
        aapt_output = subprocess.check_output(
            ['aapt', 'dump', 'badging', apk_path],
            stderr=subprocess.STDOUT
        ).decode()
        permissions = [line.split(":")[1].strip().strip("'") 
                       for line in aapt_output.splitlines() if "uses-permission:" in line]
        package = None
        label = None
        version = None
        for line in aapt_output.splitlines():
            if line.startswith("package:"):
                parts = dict(x.split("=") for x in line.split()[1:])
                package = parts.get("name", "").strip("'")
                version = parts.get("versionName", "").strip("'")
            if line.startswith("application-label:"):
                label = line.split(":", 1)[1].strip().strip("'")
        return {
            'permissions': permissions,
            'package': package,
            'label': label,
            'version': version,
            'raw_output': aapt_output
        }
    except subprocess.CalledProcessError as e:
        logging.error(f"AAPT failed: {e.output.decode()}")
        return {'error': e.output.decode()}
    except Exception as e:
        logging.error(f"General error: {str(e)}")
        return {'error': str(e)}