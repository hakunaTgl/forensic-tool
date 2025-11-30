"""AI helper module.

This module provides AI-powered assistance for permission analysis
and generating recommendations.
"""


def summarize_permissions(permissions: list) -> str:
    """Generate a summary of the provided permissions.
    
    Args:
        permissions: List of Android permission strings.
        
    Returns:
        str: Human-readable summary of the permissions.
    """
    if not permissions:
        return "No permissions found."
    
    # Handle string input
    if isinstance(permissions, str):
        permissions = [p.strip() for p in permissions.split(",")]
    
    # Count by category
    dangerous = []
    network = []
    storage = []
    location = []
    other = []
    
    for perm in permissions:
        perm_lower = perm.lower()
        if any(x in perm_lower for x in ['sms', 'contacts', 'call_log', 'camera', 'audio']):
            dangerous.append(perm)
        elif any(x in perm_lower for x in ['internet', 'network']):
            network.append(perm)
        elif any(x in perm_lower for x in ['storage', 'external']):
            storage.append(perm)
        elif 'location' in perm_lower:
            location.append(perm)
        else:
            other.append(perm)
    
    summary_parts = [f"APK requests {len(permissions)} permissions."]
    
    if dangerous:
        summary_parts.append(f"⚠️ {len(dangerous)} potentially dangerous permissions detected.")
    
    if network:
        summary_parts.append(f"Network access: {len(network)} permissions.")
    
    if location:
        summary_parts.append(f"Location access: {len(location)} permissions.")
    
    if storage:
        summary_parts.append(f"Storage access: {len(storage)} permissions.")
    
    if dangerous:
        summary_parts.append(f"Most critical: {dangerous[0]}")
    elif permissions:
        summary_parts.append(f"Primary permission: {permissions[0]}")
    
    return " ".join(summary_parts)


def get_ai_recommendation(permissions: list, risk_score: int) -> dict:
    """Get AI recommendations based on permissions and risk score.
    
    Args:
        permissions: List of Android permissions.
        risk_score: Calculated risk score.
        
    Returns:
        dict: Recommendations and analysis.
    """
    if not permissions:
        return {
            "risk_level": "none",
            "recommendation": "No permissions detected. The APK may not require any special permissions.",
            "concerns": []
        }
    
    concerns = []
    recommendations = []
    
    # Check for dangerous permissions
    dangerous_keywords = ['sms', 'contacts', 'call_log', 'camera', 'record_audio']
    for perm in permissions:
        perm_lower = perm.lower()
        for keyword in dangerous_keywords:
            if keyword in perm_lower:
                concerns.append(f"Access to {keyword.replace('_', ' ')} data")
    
    # Determine risk level
    if risk_score >= 10:
        risk_level = "critical"
        recommendations.append("Do not install this application without thorough review.")
        recommendations.append("Consider using a sandboxed environment for testing.")
    elif risk_score >= 6:
        risk_level = "high"
        recommendations.append("Review why the application needs these permissions.")
        recommendations.append("Consider alternatives with fewer permissions.")
    elif risk_score >= 3:
        risk_level = "medium"
        recommendations.append("Permissions are within normal range but review is recommended.")
    else:
        risk_level = "low"
        recommendations.append("Permission profile appears reasonable.")
    
    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "total_permissions": len(permissions),
        "concerns": concerns,
        "recommendations": recommendations
    }


def get_permission_description(permission: str) -> str:
    """Get a human-readable description of a permission.
    
    Args:
        permission: Android permission string.
        
    Returns:
        str: Description of the permission.
    """
    descriptions = {
        "android.permission.INTERNET": "Allows the app to open network connections.",
        "android.permission.ACCESS_FINE_LOCATION": "Allows precise GPS location access.",
        "android.permission.ACCESS_COARSE_LOCATION": "Allows approximate location via cell towers/WiFi.",
        "android.permission.CAMERA": "Allows access to the device camera.",
        "android.permission.RECORD_AUDIO": "Allows recording audio from the microphone.",
        "android.permission.READ_CONTACTS": "Allows reading contacts data.",
        "android.permission.WRITE_CONTACTS": "Allows modifying contacts data.",
        "android.permission.READ_SMS": "Allows reading SMS messages.",
        "android.permission.SEND_SMS": "Allows sending SMS messages.",
        "android.permission.RECEIVE_SMS": "Allows receiving and processing SMS messages.",
        "android.permission.READ_EXTERNAL_STORAGE": "Allows reading files from external storage.",
        "android.permission.WRITE_EXTERNAL_STORAGE": "Allows writing files to external storage.",
        "android.permission.READ_CALL_LOG": "Allows reading call history.",
        "android.permission.WRITE_CALL_LOG": "Allows modifying call history.",
        "android.permission.ACCESS_NETWORK_STATE": "Allows checking network connectivity.",
    }
    
    return descriptions.get(permission, f"Permission: {permission.split('.')[-1]}")
