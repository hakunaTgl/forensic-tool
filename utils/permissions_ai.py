# utils/permissions_ai.py
import joblib
import numpy as np
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default model path (can be overridden)
MODEL_PATH = os.getenv("PERMISSION_MODEL_PATH", "models/permissions_model.pkl")

# Permissions used during model training
KNOWN_PERMISSIONS = [
    'android.permission.INTERNET',
    'android.permission.READ_SMS',
    'android.permission.RECORD_AUDIO',
    'android.permission.CAMERA',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.READ_CONTACTS',
    'android.permission.WRITE_EXTERNAL_STORAGE',
    # You can append more as needed
]

# Try loading the model safely
try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Loaded model from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Could not load model: {e}")
    model = None  # Fallback for testing or diagnostics

def encode_permissions(permission_list):
    """Encodes a permission list into a binary feature array."""
    encoded = [
        1 if perm in permission_list else 0
        for perm in KNOWN_PERMISSIONS
    ]
    logger.debug(f"Encoded permissions: {encoded}")
    return np.array(encoded).reshape(1, -1)

def predict_risk(permission_list):
    """Predicts the risk score (0-100) based on permissions."""
    if model is None:
        logger.warning("Risk model not loaded; returning default risk score.")
        return 50.0  # Neutral fallback risk
    
    features = encode_permissions(permission_list)
    try:
        score = model.predict_proba(features)[0][1] * 100  # probability of class 1
        return round(score, 2)
    except Exception as e:
        logger.error(f"Risk prediction failed: {e}")
        return 0.0  # Conservative fallback if model fails