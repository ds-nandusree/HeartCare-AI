# 🏥 HeartCare AI – AI-Powered Cardiovascular Risk Prediction System

🚀 Live App: https://heartcare-ai-4bl8cajygkvvge4m2awsiw.streamlit.app/

---

## 📌 Overview
HeartCare AI is a machine learning-based web application that predicts the risk of heart disease using patient medical parameters. The system provides real-time predictions, interactive risk visualization, patient history tracking, and automated medical report generation through a Streamlit-based dashboard.

This project demonstrates the integration of **Machine Learning, Data Visualization, and Full-Stack Deployment in healthcare**.

---

## 🎯 Key Features
- ❤️ Predicts heart disease risk using Machine Learning (Random Forest)
- 📊 Interactive risk visualization using Plotly gauge charts
- 🧠 Feature importance analysis for model insight
- 🗂 Patient history storage using SQLite database
- 📄 Generates downloadable medical PDF reports
- 🔐 Simple doctor authentication system
- 🌐 Fully deployed web application using Streamlit Cloud

---

## 🛠 Tech Stack
- Python 🐍
- Streamlit 🎯
- Scikit-learn 🤖
- Pandas 📊
- NumPy 🔢
- Plotly 📈
- SQLite 🗄️
- FPDF 📄

---

## 🧠 Machine Learning Workflow
1. Data preprocessing and feature selection  
2. Model training using Random Forest Classifier  
3. Prediction of heart disease risk (binary classification)  
4. Probability scoring for risk interpretation  
5. Model-based feature importance analysis  

---

## 📊 System Architecture
User Input → Streamlit UI → ML Model Prediction → Risk Visualization → Database Storage → PDF Report Generation  

---

## 📁 Project Structure

HeartCare-AI/
│
├── app.py # Main Streamlit application
├── model.pkl # Trained ML model
├── train_model.py # Model training script
├── heart.csv # Dataset used for training
├── requirements.txt # Dependencies
└── README.md


---

## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/HeartCare-AI.git
cd HeartCare-AI
pip install -r requirements.txt
streamlit run app.py
