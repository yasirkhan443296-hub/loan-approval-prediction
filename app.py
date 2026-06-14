import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page config
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
    }
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
st.markdown("Fill in the applicant details below to predict loan approval.")
st.divider()

# ── Section 1: Personal Info ──
st.subheader("👤 Personal Information")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
with col2:
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
with col3:
    dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=1)

col4, col5 = st.columns(2)
with col4:
    education = st.selectbox("Education Level", ["High School", "Associate", "Bachelor", "Master", "Doctorate"])
with col5:
    employment = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed", "Part-Time"])

# ── Section 2: Financial Info ──
st.divider()
st.subheader("💰 Financial Information")

col1, col2 = st.columns(2)
with col1:
    annual_income = st.number_input("Annual Income (₹)", min_value=0, value=50000, step=1000)
    monthly_debt = st.number_input("Monthly Debt Payments (₹)", min_value=0, value=300, step=50)
    savings_balance = st.number_input("Savings Account Balance (₹)", min_value=0, value=5000, step=500)
    total_assets = st.number_input("Total Assets (₹)", min_value=0, value=100000, step=1000)

with col2:
    checking_balance = st.number_input("Checking Account Balance (₹)", min_value=0, value=2000, step=500)
    total_liabilities = st.number_input("Total Liabilities (₹)", min_value=0, value=20000, step=1000)
    job_tenure = st.number_input("Job Tenure (years)", min_value=0, max_value=50, value=5)
    experience = st.number_input("Total Work Experience (years)", min_value=0, max_value=50, value=10)

# ── Section 3: Credit Info ──
st.divider()
st.subheader("📊 Credit Information")

col1, col2 = st.columns(2)
with col1:
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=600)
    cc_utilization = st.slider("Credit Card Utilization Rate", 0.0, 1.0, 0.3, step=0.01)
    open_credit_lines = st.number_input("Number of Open Credit Lines", min_value=0, max_value=20, value=3)
    credit_inquiries = st.number_input("Number of Credit Inquiries", min_value=0, max_value=20, value=1)

with col2:
    credit_history_length = st.number_input("Length of Credit History (years)", min_value=0, max_value=50, value=10)
    payment_history = st.slider("Payment History Score (0-30)", 0, 30, 20)
    utility_payment = st.slider("Utility Bills Payment History (0-1)", 0.0, 1.0, 0.8, step=0.01)
    bankruptcy = st.selectbox("Bankruptcy History", ["No (0)", "Yes (1)"])

# ── Section 4: Loan Info ──
st.divider()
st.subheader("🏠 Loan & Housing Details")

col1, col2 = st.columns(2)
with col1:
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=20000, step=1000)
    loan_duration = st.selectbox("Loan Duration (months)", [12, 24, 36, 48, 60, 72, 84, 96])
    loan_purpose = st.selectbox("Loan Purpose", ["Home", "Auto", "Education", "Debt Consolidation", "Other"])

with col2:
    home_ownership = st.selectbox("Home Ownership Status", ["Own", "Rent", "Mortgage", "Other"])
    prev_defaults = st.selectbox("Previous Loan Defaults", ["No (0)", "Yes (1)"])
    base_interest = st.number_input("Base Interest Rate", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

st.divider()

# ── Derived features ──
monthly_income = annual_income / 12
debt_to_income = monthly_debt / monthly_income if monthly_income > 0 else 0
net_worth = total_assets - total_liabilities
interest_rate = base_interest + 0.01
monthly_loan_payment = (loan_amount * interest_rate / 12) / (1 - (1 + interest_rate / 12) ** -loan_duration) if loan_duration > 0 else 0
total_debt_to_income = (monthly_debt + monthly_loan_payment) / monthly_income if monthly_income > 0 else 0
risk_score = 50  # placeholder

# ── Encode categorical ──
marital_map = {"Single": 0, "Married": 1, "Divorced": 2, "Widowed": 3}
edu_map = {"High School": 0, "Associate": 1, "Bachelor": 2, "Master": 3, "Doctorate": 4}
emp_map = {"Employed": 0, "Self-Employed": 1, "Unemployed": 2, "Part-Time": 3}
home_map = {"Own": 0, "Rent": 1, "Mortgage": 2, "Other": 3}
purpose_map = {"Home": 0, "Auto": 1, "Education": 2, "Debt Consolidation": 3, "Other": 4}

# ── Predict ──
if st.button("🔍 Check Loan Eligibility"):
    input_data = pd.DataFrame([{
        'Age': age,
        'AnnualIncome': annual_income,
        'CreditScore': credit_score,
        'EmploymentStatus': emp_map[employment],
        'EducationLevel': edu_map[education],
        'Experience': experience,
        'LoanAmount': loan_amount,
        'LoanDuration': loan_duration,
        'MaritalStatus': marital_map[marital_status],
        'NumberOfDependents': dependents,
        'HomeOwnershipStatus': home_map[home_ownership],
        'MonthlyDebtPayments': monthly_debt,
        'CreditCardUtilizationRate': cc_utilization,
        'NumberOfOpenCreditLines': open_credit_lines,
        'NumberOfCreditInquiries': credit_inquiries,
        'DebtToIncomeRatio': debt_to_income,
        'BankruptcyHistory': 1 if bankruptcy == "Yes (1)" else 0,
        'LoanPurpose': purpose_map[loan_purpose],
        'PreviousLoanDefaults': 1 if prev_defaults == "Yes (1)" else 0,
        'PaymentHistory': payment_history,
        'LengthOfCreditHistory': credit_history_length,
        'SavingsAccountBalance': savings_balance,
        'CheckingAccountBalance': checking_balance,
        'TotalAssets': total_assets,
        'TotalLiabilities': total_liabilities,
        'MonthlyIncome': monthly_income,
        'UtilityBillsPaymentHistory': utility_payment,
        'JobTenure': job_tenure,
        'NetWorth': net_worth,
        'BaseInterestRate': base_interest,
        'InterestRate': interest_rate,
        'MonthlyLoanPayment': monthly_loan_payment,
        'TotalDebtToIncomeRatio': total_debt_to_income,
        'RiskScore': risk_score,
    }])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.markdown('<div class="result-box approved">✅ Loan Approved!</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown('<div class="result-box rejected">❌ Loan Not Approved</div>', unsafe_allow_html=True)

st.markdown("<br><small style='color:gray;'>Predictions are for educational purposes only.</small>", unsafe_allow_html=True)
