DANGEROUS_PERMISSIONS = {
    "android.permission.READ_SMS": 3,
    "android.permission.SEND_SMS": 3,
    "android.permission.READ_CONTACTS": 2,
    "android.permission.RECORD_AUDIO": 2,
    "android.permission.ACCESS_FINE_LOCATION": 2,
    "android.permission.CAMERA": 2,
}

def predict_risk(permissions):
    if model is None:
        raise RuntimeError("Model not loaded.")
    # Example: model expects a list of permissions as input
    return model.predict([permissions])

def assess_permissions(permissions):
    return sum(DANGEROUS_PERMISSIONS.get(p, 0) for p in permissions)
