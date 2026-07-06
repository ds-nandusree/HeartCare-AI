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
- 🌐 Fully deployed web application using Streamlit cloud

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
## 📊 Sample Output

### 🧾 Input Example
- Age: 45  
- Sex: Male  
- Chest Pain Type: 2  
- Resting BP: 120  
- Cholesterol: 200  
- Fasting Sugar: 0  
- Max Heart Rate: 150  
- Exercise Angina: 0  

---

### 🤖 Model Prediction
- Prediction: **HIGH RISK** 🚨  
- Probability: **78.34%**

---

### 📊 Risk Visualization
- A real-time gauge chart is displayed showing the patient’s heart disease risk level from 0% to 100%.
- Green → Low Risk  
- Yellow → Medium Risk  
- Red → High Risk  

---

### 📄 Medical Report Output
A downloadable PDF report is generated containing:
- Patient details  
- Model prediction result  
- Risk probability  
- Timestamp of analysis  

---

### 🗂 Patient History Output
All predictions are stored in SQLite database and displayed as a table inside the dashboard for future reference.


## 📸 Project Screenshots

### 🏠 Home Dashboard
<img width="1076" height="560" alt="Screenshot 2026-07-04 155455" src="https://github.com/user-attachments/assets/52b94b68-0204-4c36-b40c-d9628a851ed8" />


### 📊 Prediction Page
<img width="1088" height="476" alt="Screenshot 2026-07-04 155538" src="https://github.com/user-attachments/assets/0590fe8f-790e-4982-884b-8feeb0c76444" />


### 📈 Risk Visualization
<img width="1088" height="537" alt="Screenshot 2026-07-04 155524" src="https://github.com/user-attachments/assets/c1f9f22f-98d2-4301-83e0-ef57e6ef95ea" />


### 🧾 Medical Report
<img width="449" height="293" alt="Screenshot 2026-07-04 160214" src="https://github.com/user-attachments/assets/546ea296-ef58-4908-80ab-6392bbca62e6" />


## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/HeartCare-AI.git
cd HeartCare-AI
pip install -r requirements.txt
streamlit run app.py
