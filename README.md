# 🧠 AI-Based Brain Tumor Detection & Classification System

A full-stack AI web application built with **Streamlit, TensorFlow, and SQLite** that detects and classifies brain tumors from MRI scans using a deep learning model (ResNet50 + custom CNN head). The system also includes user authentication, Grad-CAM visualization, chatbot assistant, history tracking, and PDF report generation.

---

## 🚀 Features

### 🔐 Authentication System
- User Signup & Login
- Secure password hashing (SHA-256)
- Session-based login system

### 🧠 AI Tumor Detection
- Upload MRI scans (JPG, PNG, JPEG)
- Deep Learning model (ResNet50-based CNN)
- Multi-class classification:
  - Glioma
  - Meningioma
  - Pituitary Tumor
  - No Tumor

### 🔥 Explainable AI (Grad-CAM)
- Heatmap visualization of tumor regions
- Overlay on MRI images for interpretability

### 📊 Dashboard System
- Upload MRI scans
- View prediction results
- Access history, reports, chatbot, and profile

### 📜 History Tracking
- Stores all predictions in SQLite database
- View past scans with timestamps
- Download reports or delete records

### 📄 PDF Report Generation
- Patient details
- MRI scan image
- Prediction result + confidence
- Grad-CAM visualization
- Downloadable medical-style report

### 🤖 AI Chatbot Assistant
- Medical Q&A system
- Knowledge-based responses for:
  - Glioma
  - Meningioma
  - Pituitary tumors

### ⚙️ Profile Management
- Update user details
- Change password
- Download latest generated report

---

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Frontend    | Streamlit |
| Backend     | Python |
| AI Model    | TensorFlow (ResNet50 + CNN) |
| Visualization | OpenCV + Grad-CAM |
| Database    | SQLite |
| Report Gen  | ReportLab |
| Security    | SHA-256 Hashing |

---

## 📂 Project Structure
