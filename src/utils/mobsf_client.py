"""MobSF client module.

This module provides functionality to interact with the Mobile Security
Framework (MobSF) API for APK analysis.
"""

import requests
import os
import logging

logger = logging.getLogger(__name__)

MOBSF_URL = os.getenv("MOBSF_URL", "http://127.0.0.1:8000/api/v1/")
API_KEY = os.getenv("MOBSF_API_KEY", "")


def get_headers():
    """Get the authorization headers for MobSF API.
    
    Returns:
        dict: Headers dictionary with authorization.
    """
    return {'Authorization': API_KEY}


def upload_apk(filepath: str) -> dict:
    """Upload an APK file to MobSF for analysis.
    
    Args:
        filepath: Path to the APK file.
        
    Returns:
        dict: Response from MobSF API.
    """
    if not os.path.exists(filepath):
        return {"error": "File not found", "filepath": filepath}
    
    if not API_KEY:
        return {"error": "MOBSF_API_KEY not configured"}
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (os.path.basename(filepath), f)}
            response = requests.post(
                MOBSF_URL + 'upload',
                files=files,
                headers=get_headers(),
                timeout=120
            )
            response.raise_for_status()
            return response.json()
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to MobSF server")
        return {"error": "Cannot connect to MobSF server"}
    except requests.exceptions.Timeout:
        logger.error("MobSF upload timed out")
        return {"error": "Upload timed out"}
    except Exception as e:
        logger.error(f"MobSF upload error: {e}")
        return {"error": str(e)}


def scan_uploaded(scan_hash: str) -> dict:
    """Trigger a scan for an uploaded file.
    
    Args:
        scan_hash: The hash of the uploaded file.
        
    Returns:
        dict: Response from MobSF API.
    """
    if not API_KEY:
        return {"error": "MOBSF_API_KEY not configured"}
    
    try:
        data = {'hash': scan_hash}
        response = requests.post(
            MOBSF_URL + 'scan',
            data=data,
            headers=get_headers(),
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to MobSF server"}
    except Exception as e:
        logger.error(f"MobSF scan error: {e}")
        return {"error": str(e)}


def get_scan_report(scan_hash: str) -> dict:
    """Get the scan report for a previously scanned file.
    
    Args:
        scan_hash: The hash of the scanned file.
        
    Returns:
        dict: Scan report from MobSF.
    """
    if not API_KEY:
        return {"error": "MOBSF_API_KEY not configured"}
    
    try:
        params = {'hash': scan_hash}
        response = requests.get(
            MOBSF_URL + 'report_json',
            headers=get_headers(),
            params=params,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to MobSF server"}
    except Exception as e:
        logger.error(f"MobSF report error: {e}")
        return {"error": str(e)}


def check_mobsf_status() -> dict:
    """Check if MobSF server is available.
    
    Returns:
        dict: Status of MobSF server.
    """
    try:
        response = requests.get(
            MOBSF_URL.rstrip('/'),
            timeout=5
        )
        return {
            "status": "available" if response.ok else "unavailable",
            "url": MOBSF_URL
        }
    except requests.exceptions.ConnectionError:
        return {"status": "unavailable", "url": MOBSF_URL}
    except Exception as e:
        return {"status": "error", "message": str(e)}
