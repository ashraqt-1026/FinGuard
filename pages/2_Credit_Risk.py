import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Credit Risk · FinGuard 360", page_icon="🏦", layout="wide")

st.markdown("""<style>.main { background-color: #f8f9fa; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=60)
    st.markdown("## 🛡️ FinGuard 360")
    st.markdown("---")
    st.page_link("app.py", label="🏠 Home Dashboard")
    st.page_link("pages/1_Fraud_Detection.py", label="💳 Fraud Detection")
    st.page_link("pages/2_Credit_Risk.py", label="🏦 Credit Risk")
    st.page_link("pages/3_Data_Dashboard.py", label="📊 Data Dashboard")
    st.page_link("pages/4_Model_Insights.py", label="🧠 Model Insights")
    st.page_link("pages/5_Discussion.py", label="🧑‍🏫 Discussion")

@st.cache_resource
def load_model():
    model = joblib.load("Credit_risk_model/saved_models/credit_risk_model.pkl")
    meta  = joblib.load("Credit_risk_model/saved_models/credit_risk_meta.pkl")
    return model, meta

model, meta = load_model()

st.markdown("# 🏦 Credit Risk Assessment")
st.markdown("Evaluate a loan applicant's default probability and get an Approve / Reject decision.")
st.markdown("---")

with st.form("credit_form"):
    st.markdown("### 📝 Applicant Details")
    c1, c2 = st.columns(2)

    with c1:
        age        = st.number_input("Age (years)", min_value=18, max_value=100, value=30)
        income     = st.number_input("Annual Income ($)", min_value=1000, value=50000, step=1000)
        emp_length = st.number_input("Employment Length (years)", min_value=0.0, max_value=60.0, value=5.0, step=0.5)
        home_own   = st.selectbox("Home Ownership", meta['cat_values']['person_home_ownership'])

    with c2:
        loan_amnt    = st.number_input("Loan Amount ($)", min_value=500, value=10000, step=500)
        loan_int     = st.number_input("Interest Rate (%)", min_value=1.0, max_value=50.0, value=12.0, step=0.1)
        loan_intent  = st.selectbox("Loan Intent", meta['cat_values']['loan_intent'])
        loan_grade   = st.selectbox("Loan Grade", meta['cat_values']['loan_grade'])

    c3, c4 = st.columns(2)
    with c3:
        loan_pct    = st.slider("Loan % of Income", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
    with c4:
        cred_hist   = st.number_input("Credit History Length (years)", min_value=0, max_value=30, value=5)
        default_file = st.selectbox("Previous Default on File?", meta['cat_values']['cb_person_default_on_file'])

    submitted = st.form_submit_button("🏦 Predict Credit Risk", type="primary", width="stretch")

if submitted:
    errors = []
    if income < 1000:
        errors.append("Income must be at least $1,000.")
    if loan_amnt > income * 10:
        errors.append("Loan amount seems unrealistically high relative to income.")
    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    input_df = pd.DataFrame([{
        'person_age': age,
        'person_income': income,
        'person_home_ownership': home_own,
        'person_emp_length': emp_length,
        'loan_intent': loan_intent,
        'loan_grade': loan_grade,
        'loan_amnt': loan_amnt,
        'loan_int_rate': loan_int,
        'loan_percent_income': loan_pct,
        'cb_person_default_on_file': default_file,
        'cb_person_cred_hist_length': cred_hist
    }])

    proba      = float(model.predict_proba(input_df)[0][1])
    prediction = int(model.predict(input_df)[0])
    proba_pct  = proba * 100

    st.markdown("---")
    st.markdown("### 🔎 Risk Assessment Result")

    col_decision, col_details = st.columns([1, 1])

    with col_decision:
        if proba_pct < 30:
            risk_label = "🟢 Low Risk"
            decision   = "✅ APPROVED"
            dec_color  = "#34a853"
        elif proba_pct < 60:
            risk_label = "🟡 Medium Risk"
            decision   = "⚠️ CONDITIONAL REVIEW"
            dec_color  = "#fbbc04"
        else:
            risk_label = "🔴 High Risk"
            decision   = "❌ REJECTED"
            dec_color  = "#ea4335"

        st.markdown(f"""
        <div style="background:white; border-radius:12px; padding:24px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;">
            <div style="font-size:1.6rem; font-weight:800; color:{dec_color};">{decision}</div>
            <div style="font-size:1.1rem; margin-top:8px;">{risk_label}</div>
            <div style="font-size:2.5rem; font-weight:700; color:{dec_color}; margin-top:12px;">
                {proba_pct:.1f}%
            </div>
            <div style="color:#666; font-size:0.9rem;">Default Probability</div>
        </div>
        """, unsafe_allow_html=True)

    with col_details:
        st.markdown("**Risk Factors Summary**")
        factors = pd.DataFrame({
            'Factor': ['Loan Grade', 'Interest Rate', 'Loan % of Income', 'Previous Default', 'Employment Length'],
            'Value':  [loan_grade, f"{loan_int}%", f"{loan_pct*100:.0f}%", default_file, f"{emp_length} yrs"]
        })
        st.dataframe(factors, hide_index=True, width="stretch")

        st.markdown("**Default Probability Gauge**")
        if proba_pct < 30:
            bar_color = "#34a853"
        elif proba_pct < 60:
            bar_color = "#fbbc04"
        else:
            bar_color = "#ea4335"

        st.markdown(f"""
        <div style="background:#e0e0e0; border-radius:8px; height:24px; overflow:hidden; margin-top:8px;">
            <div style="width:{proba_pct:.1f}%; background:{bar_color}; height:100%; border-radius:8px;
                        display:flex; align-items:center; justify-content:center;
                        color:white; font-weight:700; font-size:0.85rem;">
                {proba_pct:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)