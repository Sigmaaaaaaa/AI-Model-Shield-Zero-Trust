import streamlit as st
import requests
import json 
from PIL import Image
import io

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/predict"
st.set_page_config(page_title="Thales AI Model Shield Demo", layout="wide")

st.title("🛡️ AI Model Shield: Trusted Inference Demo")
st.markdown("### Zero-Trust, AI-Powered Protection for Critical Systems")
st.markdown("---")

# --- Security Inputs ---
col1, col2 = st.columns(2)
with col1:
    api_key_input = st.text_input("Zero-Trust API Key (X-API-Key)", 
                                 placeholder="Enter the secret key for access",
                                 type="password")
with col2:
    uploaded_file = st.file_uploader("Upload Satellite Image (224x224)", 
                                     type=["jpg", "jpeg", "png"])

st.markdown("---")

# --- Inference Button ---
if st.button("🚀 Run Secure Inference", type="primary"):
    
    # 1. Client-Side Input Checks (Basic Zero-Trust Gate)
    if not api_key_input:
        st.error("ACCESS DENIED: Please enter the API Key (Zero-Trust Violation).")
        st.stop()
    if not uploaded_file:
        st.warning("Please upload an image.")
        st.stop()
        
    # 2. Prepare Data and Headers for FastAPI
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    # The X-API-Key header is the key to passing Zero-Trust Auth on the server side
    headers = {"X-API-Key": api_key_input}
    
    with st.spinner("Running through Security Chain (Auth, Validation, Decryption)..."):
        
        # 3. Call the Secure API Endpoint
        try:
            response = requests.post(API_URL, files=files, headers=headers)
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: FastAPI server is not running or is inaccessible.")
            st.warning("Please ensure Uvicorn is running in the separate terminal.")
            st.stop()

    # 4. Process Response
    st.markdown("## 📊 Shield Analysis Result")
    
    # --- Server-Side Authentication Failure ---
    if response.status_code == 401:
        st.error(f"❌ AUTHENTICATION FAILURE (Code 401): Invalid or missing API Key.")
        st.warning("This demonstrates the **Zero-Trust Digital Identity** enforcement.")
    
    # --- Successful Response ---
    elif response.status_code == 200:
        results = response.json()
        
        # Display Input Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Input Image (Validated)", width=250)
        
        # Check for CRITICAL Data Poisoning Alert
        if results.get("trust_score", 0) == 0.0 and results.get("status") == "CRITICAL ALERT":
            st.error("🚨 CRITICAL ALERT: INFERENCE REJECTED")
            st.subheader(f"Data Integrity Failure: {results.get('reason', 'Unknown error.')}")
            st.warning("This demonstrates the **Data Poisoning Detection** layer in action.")
            st.metric("Trust Score", results['trust_score'])
        
        # Secure Success Case (All Security Checks Cleared)
        else:
            trust_score = results.get('trust_score', 0)
            
            st.success("✅ SECURITY PASS: Request Cleared for Inference")
            st.progress(trust_score / 100, text=f"Trust Level: {trust_score:.2f}%")
            
            col_a, col_b = st.columns(2)
            
            # **THE FIX**: Reading the new 'prediction_name' field
            col_a.metric("Predicted Class Index", results.get('prediction_name', 'N/A')) 
            
            col_b.metric("Model Confidence", f"{results.get('confidence', 0)}%")
            
            st.markdown("### Explainable Trust (XAI)")
            st.code(results.get('explanation', 'No explanation generated.'), language='python')
            st.caption("This explanation provides critical decision support for Defence/Aeronautics operators.")

    # --- Unexpected Server Error ---
    else:
        st.error(f"An unexpected API error occurred (Code {response.status_code}).")
        st.json(response.json())