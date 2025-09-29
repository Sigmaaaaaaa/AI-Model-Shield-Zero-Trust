import os
import sys
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

# Import Custom Modules
from src.model_loader import load_secure_model
from src.validator import validate_image_integrity
# NOTE: get_model_explanation is updated to return predicted_class and explanation
from src.xai_engine import calculate_trust_score, get_model_explanation, preprocess_image

# --- Load Environment Variables ---
load_dotenv()
API_KEY_SECRET = os.getenv("API_KEY")

# --- FastAPI Setup ---
app = FastAPI(
    title="Thales AI Model Shield API",
    description="A Zero-Trust service for secure, explainable AI inference.",
    version="1.0.0"
)

# --- Zero-Trust Authentication Implementation ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(api_key_header)):
    """Enforces the Zero-Trust policy on every incoming request."""
    if api_key == API_KEY_SECRET:
        return api_key
    # Raise 401 Unauthorized if key is missing or incorrect
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Zero-Trust Policy Violation: Invalid or Missing X-API-Key header."
    )

# --- Startup Event: Secure Model Decryption and Loading ---

@app.on_event("startup")
async def startup_event():
    """Decrypts the model IP and loads it into the application state."""
    print("\n[SHIELD STARTUP]: Initiating secure model decryption...")
    
    # Call the decryption and loading function from src/model_loader.py
    model = load_secure_model()
    
    if model:
        app.state.model = model
        print("\n[SHIELD STARTUP]: Model loaded and ready for secure inference.")
    else:
        print("\n[SHIELD STARTUP]: FATAL ERROR - Model decryption/loading failed. Check keys and encrypted file.")
        app.state.model = None


# --- Health Check Endpoint ---

@app.get("/", tags=["Monitoring"])
def read_root():
    """Simple health check to verify server status."""
    if app.state.model is not None:
        return {"status": "Model Shield Server Running", "model_ip_status": "SECURELY LOADED"}
    return {"status": "Server Running", "model_ip_status": "FATAL ERROR (Not Loaded)"}


# --- Secure Prediction Endpoint (The Core Feature) ---

@app.post("/predict", tags=["Secure Inference"])
async def secure_predict(
    file: UploadFile = File(..., description="Satellite image payload (224x224)"),
    # This dependency ensures the API key is validated before ANY code proceeds
    auth: str = Depends(get_api_key) 
):
    """
    Runs an image through the full security chain and generates a Trust Score.
    """
    if app.state.model is None:
         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model Shield is offline: Model load failed.")
         
    # 1. READ INPUT BYTES
    image_bytes = await file.read()
    
    # 2. DATA POISONING DETECTION (from src/validator.py)
    is_valid, validation_reason = validate_image_integrity(image_bytes)
    
    if not is_valid:
        # CRITICAL ALERT: Reject immediately upon validation failure
        return {
            "status": "CRITICAL ALERT",
            "trust_score": 0.0,
            "prediction_name": "REJECTED (Data Integrity Failure)", # Updated field name
            "confidence": 0.0,
            "alert": validation_reason
        }

    # --- SECURITY CHECKS PASSED: PROCEED TO INFERENCE ---

    # 3. PREPROCESS IMAGE (from src/xai_engine.py)
    try:
        image_preprocessed = preprocess_image(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Image preprocessing failed: {e}")

    # 4. SECURE INFERENCE
    predictions = app.state.model.predict(image_preprocessed, verbose=0)
    confidence = np.max(predictions[0])
    
    # 5. XAI AND TRUST SCORE CALCULATION
    # NOTE THE CHANGE: Capturing two return values
    predicted_class, explanation = get_model_explanation(app.state.model, image_preprocessed) 
    
    trust_score = calculate_trust_score(float(confidence), is_valid)
    
    # 6. RETURN SECURE RESPONSE
    return {
        "status": "SECURE INFERENCE SUCCESS",
        "trust_score": trust_score, 
        "confidence": round(float(confidence) * 100, 2),
        "alert": validation_reason, # Should be "Data integrity passed."
        "prediction_name": predicted_class, # NEW FIELD USED BY DASHBOARD
        "explanation": explanation
    }