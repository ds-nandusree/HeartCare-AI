import streamlit as st
import numpy as np
import pickle
import sqlite3
from datetime import datetime
import plotly.graph_objects as go
import shap
import pandas as pd
from fpdf import FPDF

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="HeartCare AI",
    page_icon="🏥",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

explainer = shap.TreeExplainer(model)

# =========================
# DB
# =========================
conn = sqlite3.connect("patients.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    age INTEGER,
    sex INTEGER,
    cp INTEGER,
    trestbps INTEGER,
    chol INTEGER,
    fbs INTEGER,
    restecg INTEGER,
    thalach INTEGER,
    exang INTEGER,
    oldpeak REAL,
    slope INTEGER,
    ca INTEGER,
    thal INTEGER,
    prediction INTEGER,
    probability REAL
)
""")
conn.commit()

# =========================
# LOGIN
# =========================
st.sidebar.title("🔐 Doctor Login")
user = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if user != "doctor" or password != "admin123":
    st.warning("Login required")
    st.stop()

st.sidebar.success("Logged in")

# =========================
# HEADER (CLEAN DASHBOARD)
# =========================
st.markdown("""
    <h1 style='text-align:center; color:#1f77b4;'>🏥 HeartCare AI System</h1>
    <p style='text-align:center; color:gray;'>Clinical Decision Support Dashboard</p>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Model Accuracy", "88.3%")
c2.metric("Model Type", "Random Forest")
c3.metric("Features", "13")
c4.metric("Status", "ACTIVE")

st.divider()

# =========================
# INPUT UI
# =========================
st.subheader("🧾 Patient Input Panel")

left, right = st.columns(2)

with left:
    age = st.number_input("Age", 1, 120, 45)
    sex = 1 if st.selectbox("Gender", ["Male", "Female"]) == "Male" else 0
    cp = st.selectbox("Chest Pain Type", [0,1,2,3])
    trestbps = st.number_input("Resting BP", 80, 220, 120)
    chol = st.number_input("Cholesterol", 100, 600, 200)
    fbs = st.selectbox("Fasting Sugar", [0,1])
    restecg = st.selectbox("ECG Result", [0,1,2])

with right:
    thalach = st.number_input("Max Heart Rate", 60, 220, 150)
    exang = st.selectbox("Exercise Angina", [0,1])
    oldpeak = st.number_input("ST Depression", 0.0, 10.0, 1.0)
    slope = st.selectbox("Slope", [0,1,2])
    ca = st.selectbox("Major Vessels", [0,1,2,3])
    thal = st.selectbox("Thalassemia", [0,1,2,3])

predict = st.button("❤️ Predict Risk", use_container_width=True)

# =========================
# PDF (PROFESSIONAL STYLE)
# =========================
def generate_pdf(data, prediction, prob):

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "HeartCare AI Medical Report", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Generated: {datetime.now()}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Patient Details:", ln=True)

    pdf.set_font("Arial", "", 12)
    for k, v in data.items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)

    result = "HIGH RISK" if prediction == 1 else "LOW RISK"
    pdf.cell(0, 10, f"Prediction: {result}", ln=True)
    pdf.cell(0, 10, f"Probability: {prob*100:.2f}%", ln=True)

    file = "report.pdf"
    pdf.output(file)
    return file

# =========================
# PREDICTION
# =========================
if predict:

    input_data = np.array([[age, sex, cp, trestbps, chol, fbs,
                            restecg, thalach, exang, oldpeak,
                            slope, ca, thal]])

    with st.spinner("Analyzing patient data..."):
        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

    # -------------------------
    # GAUGE (PRETTY)
    # -------------------------
    st.subheader("📊 Risk Analysis")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        title={"text": "Heart Risk Level"},
        gauge={
            "axis": {"range": [0,100]},
            "steps": [
                {"range": [0,30], "color":"#2ecc71"},
                {"range": [30,70], "color":"#f1c40f"},
                {"range": [70,100], "color":"#e74c3c"},
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # RESULT CARD
    if prediction == 1:
        st.error("🚨 HIGH CARDIAC RISK DETECTED")
    else:
        st.success("✅ LOW RISK - NORMAL CONDITION")

    # =========================
    # SHAP (SAFE)
    # =========================
    st.subheader("🧠 Feature Contribution (AI Explainability)")

    feature_names = [
        "age","sex","cp","trestbps","chol","fbs",
        "restecg","thalach","exang","oldpeak","slope","ca","thal"
    ]

    shap_values = explainer.shap_values(input_data)

    shap_vals = shap_values[1] if isinstance(shap_values, list) else shap_values
    shap_vals = np.array(shap_vals).flatten()

    min_len = min(len(feature_names), len(shap_vals))

    shap_df = pd.DataFrame({
        "Feature": feature_names[:min_len],
        "Impact": shap_vals[:min_len]
    })

    shap_df["AbsImpact"] = np.abs(shap_df["Impact"])
    shap_df = shap_df.sort_values("AbsImpact", ascending=False)

    st.dataframe(shap_df, use_container_width=True)

    # =========================
    # SAVE DB
    # =========================
    c.execute("""
    INSERT INTO records VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        str(datetime.now()), age, sex, cp, trestbps, chol, fbs,
        restecg, thalach, exang, oldpeak, slope, ca, thal,
        int(prediction), float(prob)
    ))
    conn.commit()

    # =========================
    # PDF DOWNLOAD
    # =========================
    data_dict = {
        "Age": age,
        "Gender": sex,
        "CP": cp,
        "BP": trestbps,
        "Cholesterol": chol
    }

    pdf_file = generate_pdf(data_dict, prediction, prob)

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download Medical Report", f, file_name="Heart_Report.pdf")

# =========================
# HISTORY TABLE
# =========================
st.subheader("🗂 Patient History")

history = pd.read_sql_query("SELECT * FROM records", conn)
st.dataframe(history, use_container_width=True)