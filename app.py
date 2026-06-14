import streamlit as st
import pickle
import numpy as np

# Page config
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
    }
    .stButton>button:hover { background-color: #1558b0; }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
    }
    .approved { background-color: #d4edda; color: #155724; border: 2px solid #28a745; }
    .rejected { background-color: #f8d7da; color: #721c24; border: 2px solid #dc3545; }
    </style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

# Title
st.title("🏦 Loan Approval Prediction")
st.markdown("Fill in the details below to check loan eligibility.")
st.divider()

# Input form
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    credit_history = st.selectbox("Credit History", ["Good (1)", "Bad (0)"])

with col2:
    applicant_income = st.number_input("Applicant Income (₹)", min_value=0, value=5000, step=500)
    coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, value=0, step=500)
    loan_amount = st.number_input("Loan Amount (in thousands ₹)", min_value=0, value=150, step=10)
    loan_term = st.selectbox("Loan Amount Term (months)", [360, 120, 180, 240, 300, 480, 60, 36, 84])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

st.divider()

# Encode inputs
def encode_inputs():
    gender_val = 1 if gender == "Male" else 0
    married_val = 1 if married == "Yes" else 0
    dep_map = {"0": 0, "1": 1, "2": 2, "3+": 3}
    dep_val = dep_map[dependents]
    edu_val = 0 if education == "Graduate" else 1
    self_emp_val = 1 if self_employed == "Yes" else 0
    credit_val = 1 if credit_history == "Good (1)" else 0
    area_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}
    area_val = area_map[property_area]

    return np.array([[
        gender_val, married_val, dep_val, edu_val,
        self_emp_val, applicant_income, coapplicant_income,
        loan_amount, loan_term, credit_val, area_val
    ]])

# Predict
if st.button("Check Loan Eligibility"):
    input_data = encode_inputs()
    prediction = model.predict(input_data)[0]

    if prediction == 1 or prediction == "Y":
        st.markdown('<div class="result-box approved">✅ Loan Approved!</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown('<div class="result-box rejected">❌ Loan Not Approved</div>', unsafe_allow_html=True)

st.markdown("<br><small style='color:gray;'>Model predictions are for educational purposes only.</small>", unsafe_allow_html=True)
    
