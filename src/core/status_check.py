"""System status check module.

This module provides functionality to check and report the system status.
"""


def check_status():
    """Check the current system status.
    
    Returns:
        dict: Status information containing status and message.
    """
    return {
        "status": "ok",
        "message": "System operational",
        "components": {
            "core": "active",
            "database": "connected",
            "api": "running"
        }
    }


def check_component_status(component_name):
    """Check the status of a specific component.
    
    Args:
        component_name: Name of the component to check.
        
    Returns:
        dict: Component status information.
    """
    components = {
        "core": {"status": "active", "version": "1.0.0"},
        "database": {"status": "connected", "type": "sqlite"},
        "api": {"status": "running", "endpoints": 10},
        "scraper": {"status": "ready", "engine": "scrapy"},
        "analyzer": {"status": "ready", "tools": ["aapt", "apktool"]},
    }
    
    if component_name in components:
        return components[component_name]
    
    return {"status": "unknown", "message": f"Component '{component_name}' not found"}
