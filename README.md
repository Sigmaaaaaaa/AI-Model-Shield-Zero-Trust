# 🛡️ AI Model Shield: Zero-Trust & Trusted AI Pipeline

This project implements a **multi-layered security and assurance framework** for critical AI inference pipelines. It addresses the themes of **Cybersecurity** and **Flight of the Future**, ensuring **data integrity, IP protection, and human trust**—all essential for Thales’s **Defence, Aerospace, and Digital Identity** domains.

---

## 💡 Core Value Proposition: Enabling Trusted AI

The AI Model Shield transforms AI systems from “black boxes” into **trusted decision-support tools** by enforcing three non-negotiable layers of protection:

1. **Model Theft Prevention (Cybersecurity)** → Encrypts proprietary AI weights at rest.
2. **Zero-Trust Access (Digital Identity)** → Every request authenticated with API key.
3. **Data Poisoning Detection (AI Safety)** → Validates schema & size to block corrupted/malicious inputs.

*Why it matters*: Defence and aerospace systems cannot rely on opaque AI decisions. AI Model Shield ensures **explainability, resilience, and trustworthiness** in every inference.

---

## ⚙️ Technical Architecture

| Component       | Technology                | Function & Security Role                                  | Thales Alignment            |
| --------------- | ------------------------- | --------------------------------------------------------- | --------------------------- |
| **Backend API** | FastAPI, Uvicorn          | Orchestrates Auth → Decrypt → Validate → Infer            | Scalability (Microservices) |
| **Model IP**    | MobileNetV2 (.h5 weights) | Encrypted with AES-256-CFB (`models/encrypted_model.bin`) | Model Theft Prevention      |
| **Secrets**     | `.env` file               | Simulated secure HSM for key management                   | Digital Identity            |
| **Validation**  | Custom Python logic       | Input check: `224x224, RGB, size threshold`               | AI Model Safety             |
| **Trust Score** | NumPy + Custom Logic      | Confidence × Integrity → Assurance metric                 | Defence & Security (XAI)    |

---

## 🚀 Setup & Local Execution

### Prerequisites

* Python **3.9+**
* Install all libraries from `requirements.txt`

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Secrets

Create a `.env` file in the project root:

```ini
MODEL_ENCRYPTION_KEY=
API_KEY=
```

### Step 3: Start Secure API Server (Backend)

This step decrypts the model on startup:

```bash
python -m uvicorn src.main:app
```

Expected log:

```
Model decryption successful. Model loaded in memory.
```

### Step 4: Start Demonstration Dashboard (Frontend)

In a new terminal:

```bash
python -m streamlit run dashboard/app.py
```

---

## 🔎 Demonstration Guide for Judges

Challenge the system with the scenarios below (using provided API Key: `thales_secure_access_team_alpha_2025`).

| Scenario                     | Input                                  | Expected Result                                                                                   | Feature Proved       |
| ---------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------- |
| **A. Zero-Trust Violation**  | Wrong/missing API key                  | `401 Authentication Failure`                                                                      | Zero-Trust enforced  |
| **B. Data Poisoning Attack** | Valid key + corrupted image            | `CRITICAL ALERT`, Trust Score: `0.0`                                                              | Data Integrity layer |
| **C. Secure Success**        | Valid key + `success_demo_224_rgb.jpg` | Security Pass → High Trust Score (e.g., 92.7%) → Classified output: *Cargo Ship (Maritime Asset)* | End-to-End Assurance |

---

## 📌 Closing Note

AI Model Shield demonstrates how **Zero-Trust Security + Trusted AI** can safeguard mission-critical pipelines. It lays the foundation for **secure, explainable, and operationally reliable AI** in the defence and aerospace domains.

**Developer:** Satyam Pal
**Date:** September 28, 2025
