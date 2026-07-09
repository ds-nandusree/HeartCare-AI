import streamlit as st
import numpy as np
import pandas as pd
import pickle
import sqlite3

from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HeartCare AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD MODEL
# ============================================================

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ============================================================
# DATABASE
# ============================================================

conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records(
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

# ============================================================
# SIDEBAR LOGIN
# ============================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/heart-with-pulse.png",
    width=80
)

st.sidebar.title("Doctor Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input(
    "Password",
    type="password"
)

if username != "doctor" or password != "admin123":
    st.warning("🔐 Please login to access the dashboard.")
    st.stop()

st.sidebar.success("Login Successful")

st.sidebar.markdown("---")

st.sidebar.info(
"""
**HeartCare AI**

AI-powered Clinical Decision
Support System.

Built using

• Streamlit

• Random Forest

• Plotly

• SQLite
"""
)

# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#0F62FE,#42BE65);
padding:30px;
border-radius:18px;
text-align:center;
color:white;
">

<h1>❤️ HeartCare AI</h1>

<h3>AI-Powered Cardiovascular Risk Prediction System</h3>

<p>
Helping healthcare professionals assess
heart disease risk using Machine Learning.
</p>

</div>
""",
unsafe_allow_html=True)

st.write("")

# ============================================================
# DASHBOARD METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎯 Model Accuracy",
        "88.3%"
    )

with col2:
    st.metric(
        "🤖 Model",
        "Random Forest"
    )

with col3:
    st.metric(
        "📊 Features",
        "13"
    )

with col4:
    st.metric(
        "🟢 Status",
        "Active"
    )

st.divider()

# ============================================================
# PATIENT INFORMATION
# ============================================================

st.subheader("🩺 Patient Clinical Information")

left, right = st.columns(2)

# ---------------- Left ---------------- #

with left:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=45
    )

    sex = 1 if st.selectbox(
        "Gender",
        ["Male", "Female"]
    ) == "Male" else 0

    cp = st.selectbox(
        "Chest Pain Type",
        [0,1,2,3],
        help="""
0 = Typical Angina

1 = Atypical Angina

2 = Non-anginal Pain

3 = Asymptomatic
"""
    )

    trestbps = st.number_input(
        "Resting Blood Pressure",
        80,
        220,
        120
    )

    chol = st.number_input(
        "Serum Cholesterol",
        100,
        600,
        200
    )

    fbs = st.selectbox(
        "Fasting Blood Sugar (>120 mg/dl)",
        [0,1]
    )

    restecg = st.selectbox(
        "Resting ECG",
        [0,1,2]
    )

# ---------------- Right ---------------- #

with right:

    thalach = st.number_input(
        "Maximum Heart Rate",
        60,
        220,
        150
    )

    exang = st.selectbox(
        "Exercise Induced Angina",
        [0,1]
    )

    oldpeak = st.number_input(
        "ST Depression",
        0.0,
        10.0,
        1.0
    )

    slope = st.selectbox(
        "Slope",
        [0,1,2]
    )

    ca = st.selectbox(
        "Major Vessels",
        [0,1,2,3]
    )

    thal = st.selectbox(
        "Thalassemia",
        [0,1,2,3]
    )

st.divider()

st.markdown("## 🔍 AI Prediction")

predict = st.button(
    "❤️ Predict Heart Disease Risk",
    use_container_width=True
)
# ============================================================
# PREDICTION
# ============================================================

if predict:

    input_data = np.array([[
        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal
    ]])

    with st.spinner("🩺 AI is analyzing patient data..."):

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

    st.success("Prediction Completed Successfully!")

    st.divider()

    # ============================================================
    # RISK ANALYSIS
    # ============================================================

    st.subheader("📊 Heart Disease Risk Analysis")

    gauge = go.Figure(go.Indicator(

        mode="gauge+number",

        value=probability * 100,

        number={
            "suffix": "%"
        },

        title={
            "text": "<b>Predicted Risk</b>"
        },

        gauge={

            "axis": {
                "range": [0,100]
            },

            "bar": {
                "color":"darkred"
            },

            "steps":[

                {
                    "range":[0,30],
                    "color":"#2ecc71"
                },

                {
                    "range":[30,70],
                    "color":"#f1c40f"
                },

                {
                    "range":[70,100],
                    "color":"#e74c3c"
                }

            ]

        }

    ))

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # ============================================================
    # METRICS
    # ============================================================

    m1, m2 = st.columns(2)

    with m1:

        st.metric(

            label="🎯 Prediction Confidence",

            value=f"{probability*100:.2f}%"

        )

    with m2:

        risk = "High Risk" if prediction == 1 else "Low Risk"

        st.metric(

            label="❤️ Risk Category",

            value=risk

        )

    st.divider()

    # ============================================================
    # RESULT CARD
    # ============================================================

    if prediction == 1:

        st.error("""

### 🚨 High Cardiac Risk Detected

The AI model predicts that the patient may have a **high probability of cardiovascular disease**.

### Recommendation

• Consult a Cardiologist

• Schedule further diagnostic tests

• Monitor blood pressure regularly

• Follow a healthy lifestyle

""")

    else:

        st.success("""

### ✅ Low Cardiac Risk

The patient currently appears to have a **low probability of heart disease**.

### Recommendation

• Maintain a healthy lifestyle

• Continue regular exercise

• Eat a balanced diet

• Attend routine medical check-ups

""")

    # ============================================================
    # FEATURE IMPORTANCE
    # ============================================================

    st.subheader("📈 Model Feature Importance")

    feature_names = [

        "Age",
        "Gender",
        "Chest Pain",
        "Resting BP",
        "Cholesterol",
        "Fasting Sugar",
        "ECG",
        "Max Heart Rate",
        "Exercise Angina",
        "ST Depression",
        "Slope",
        "Major Vessels",
        "Thalassemia"

    ]

    importance = model.feature_importances_

    feature_df = pd.DataFrame({

        "Feature": feature_names,

        "Importance": importance

    }).sort_values(

        "Importance",

        ascending=False

    )

    st.dataframe(

        feature_df,

        use_container_width=True,

        hide_index=True

    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=feature_df["Importance"],

            y=feature_df["Feature"],

            orientation="h"

        )

    )

    fig.update_layout(

        title="Feature Importance",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ============================================================
    # SAVE RECORD
    # ============================================================

    cursor.execute("""

    INSERT INTO records

    VALUES(

    NULL,

    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

    )

    """,

    (

        str(datetime.now()),

        age,

        sex,

        cp,

        trestbps,

        chol,

        fbs,

        restecg,

        thalach,

        exang,

        oldpeak,

        slope,

        ca,

        thal,

        int(prediction),

        float(probability)

    )

    )

    conn.commit()
# ============================================================
# PDF REPORT GENERATOR
# ============================================================

def generate_pdf(data, prediction, probability):

    pdf = FPDF()

    pdf.add_page()

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    pdf.set_font("Arial", "B", 18)

    pdf.cell(
        0,
        12,
        "HeartCare AI Medical Report",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    pdf.cell(
        0,
        8,
        f"Generated on : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        ln=True
    )

    pdf.ln(4)

    # --------------------------------------------------------
    # PATIENT DETAILS
    # --------------------------------------------------------

    pdf.set_font("Arial", "B", 13)

    pdf.cell(
        0,
        8,
        "Patient Clinical Information",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    for key, value in data.items():

        pdf.cell(
            0,
            8,
            f"{key}: {value}",
            ln=True
        )

    pdf.ln(5)

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    pdf.set_font("Arial", "B", 13)

    pdf.cell(
        0,
        8,
        "Prediction Result",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    result = "HIGH CARDIAC RISK" if prediction == 1 else "LOW CARDIAC RISK"

    pdf.cell(
        0,
        8,
        f"Prediction : {result}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Confidence : {probability*100:.2f}%",
        ln=True
    )

    pdf.ln(5)

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    pdf.set_font("Arial", "B", 12)

    pdf.cell(
        0,
        8,
        "Medical Disclaimer",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(

        0,

        7,

        "This report is generated using a Machine Learning model and is intended "
        "only for educational and clinical decision support purposes. "
        "It should not replace diagnosis or treatment by a qualified medical professional."

    )

    pdf.ln(5)

    pdf.set_font("Arial", "I", 10)

    pdf.cell(

        0,

        8,

        "Generated by HeartCare AI",

        align="C"

    )

    filename = "Heart_Report.pdf"

    pdf.output(filename)

    return filename


# ============================================================
# DOWNLOAD REPORT
# ============================================================

if predict:

    patient = {

        "Age": age,

        "Gender": "Male" if sex == 1 else "Female",

        "Chest Pain": cp,

        "Resting BP": trestbps,

        "Cholesterol": chol,

        "Fasting Blood Sugar": fbs,

        "ECG": restecg,

        "Maximum Heart Rate": thalach,

        "Exercise Angina": exang,

        "ST Depression": oldpeak,

        "Slope": slope,

        "Major Vessels": ca,

        "Thalassemia": thal

    }

    pdf_file = generate_pdf(

        patient,

        prediction,

        probability

    )

    with open(pdf_file, "rb") as pdf:

        st.download_button(

            "📄 Download Medical Report",

            pdf,

            file_name="Heart_Report.pdf",

            use_container_width=True

        )

# ============================================================
# PATIENT HISTORY
# ============================================================

st.divider()

st.subheader("📚 Patient Records")

history = pd.read_sql_query(

    "SELECT * FROM records",

    conn

)

if history.empty:

    st.info("No patient records available.")

else:

    total = len(history)

    high = len(history[history["prediction"] == 1])

    low = len(history[history["prediction"] == 0])

    avg_prob = history["probability"].mean() * 100

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("👨‍⚕️ Total Records", total)

    c2.metric("🚨 High Risk", high)

    c3.metric("✅ Low Risk", low)

    c4.metric("📊 Avg Confidence", f"{avg_prob:.1f}%")

    st.write("")

    st.dataframe(

        history,

        use_container_width=True,

        hide_index=True

    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("""

<div style="text-align:center;color:gray;">

<h4>❤️ HeartCare AI</h4>

<p>

AI-Powered Cardiovascular Risk Prediction System

</p>

<p>

Developed using

<strong>Python • Streamlit • Scikit-Learn • Plotly • SQLite</strong>

</p>

<p>

© 2026 Nandusree | Built for AI & Data Analytics Portfolio

</p>

</div>

""", unsafe_allow_html=True)
