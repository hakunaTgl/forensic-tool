"""Permission risk assessment module.

This module provides functionality to assess the risk level of Android
application permissions using predefined risk scores.
"""

# Risk scores for dangerous Android permissions
# Higher scores indicate higher risk
DANGEROUS_PERMISSIONS = {
    "android.permission.READ_SMS": 3,
    "android.permission.SEND_SMS": 3,
    "android.permission.RECEIVE_SMS": 3,
    "android.permission.READ_CONTACTS": 2,
    "android.permission.WRITE_CONTACTS": 2,
    "android.permission.RECORD_AUDIO": 2,
    "android.permission.ACCESS_FINE_LOCATION": 2,
    "android.permission.ACCESS_COARSE_LOCATION": 1,
    "android.permission.CAMERA": 2,
    "android.permission.READ_CALL_LOG": 3,
    "android.permission.WRITE_CALL_LOG": 3,
    "android.permission.READ_EXTERNAL_STORAGE": 1,
    "android.permission.WRITE_EXTERNAL_STORAGE": 2,
    "android.permission.INTERNET": 1,
    "android.permission.ACCESS_NETWORK_STATE": 1,
}


def assess_permissions(permissions):
    """Assess the cumulative risk score for a list of permissions.
    
    Args:
        permissions: List of Android permission strings.
        
    Returns:
        int: Total risk score based on the permissions.
        
    Example:
        >>> perms = ["android.permission.READ_SMS", "android.permission.CAMERA"]
        >>> assess_permissions(perms)
        5
    """
    if not permissions:
        return 0
    
    if isinstance(permissions, str):
        # Handle comma-separated string
        permissions = [p.strip() for p in permissions.split(",")]
    
    return sum(DANGEROUS_PERMISSIONS.get(p, 0) for p in permissions)


def get_risk_level(score):
    """Get a human-readable risk level based on score.
    
    Args:
        score: Numeric risk score.
        
    Returns:
        str: Risk level description.
    """
    if score == 0:
        return "None"
    elif score <= 3:
        return "Low"
    elif score <= 6:
        return "Medium"
    elif score <= 10:
        return "High"
    else:
        return "Critical"


def get_permission_details(permissions):
    """Get detailed information about each permission.
    
    Args:
        permissions: List of Android permission strings.
        
    Returns:
        list: List of dictionaries with permission details.
    """
    if not permissions:
        return []
    
    if isinstance(permissions, str):
        permissions = [p.strip() for p in permissions.split(",")]
    
    details = []
    for perm in permissions:
        risk = DANGEROUS_PERMISSIONS.get(perm, 0)
        details.append({
            "permission": perm,
            "risk_score": risk,
            "risk_level": get_risk_level(risk),
            "is_dangerous": risk >= 2
        })
    
    return details
