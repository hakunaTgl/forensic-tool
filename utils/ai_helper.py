def summarize_permissions(permissions):
    if not permissions:
        return "No permissions found."
    return f"APK requests {len(permissions)} permissions. Most critical: {permissions[0]}"