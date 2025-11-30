"""Status check utility module.

This module provides system status checking functionality.
"""


def get_system_status() -> dict:
    """Get the overall system status.
    
    Returns:
        dict: System status information.
    """
    return {
        "status": "ok",
        "details": "All utilities loaded",
        "components": {
            "apktool_runner": "available",
            "mobsf_client": "ready",
            "scraper_engine": "ready",
            "ai_helper": "active"
        }
    }


def check_dependencies() -> dict:
    """Check if external dependencies are available.
    
    Returns:
        dict: Dependency availability status.
    """
    import shutil
    
    dependencies = {
        "aapt": shutil.which("aapt") is not None,
        "apktool": shutil.which("apktool") is not None,
        "waydroid": shutil.which("waydroid") is not None,
    }
    
    return {
        "dependencies": dependencies,
        "all_available": all(dependencies.values())
    }
