import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

from  Fraud_Detection_Model.src.model import make_prediction

st.set_page_config(page_title="Fraud Detection · FinGuard 360", page_icon="💳", layout="wide")


st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .gauge-container { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=60)
    st.markdown("## 🛡️ FinGuard 360")
    st.markdown("---")
    # الروابط دي بتشتغل أوتوماتيك لو الفولدرات مترتبة صح
    st.page_link("app.py",                      label="🏠 Home Dashboard")
    st.page_link("pages/1_Fraud_Detection.py",  label="💳 Fraud Detection")
    st.page_link("pages/2_Credit_Risk.py",      label="🏦 Credit Risk")

# ── Header ────────────────────────────────────────────────────────
st.markdown("# 💳 Fraud Detection")
st.markdown("Enter transaction details to check for suspicious activity.")
st.markdown("---")

# ── Input Form ────────────────────────────────────────────────────
with st.form("fraud_form"):
    st.markdown("### 📝 Transaction Details")
    c1, c2 = st.columns(2)

    with c1:
        step      = st.number_input("Step (Time in Hours)", min_value=1, value=1, step=1)
        t_type    = st.selectbox("Transaction Type", options=['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN'])
        amount    = st.number_input("Amount ($)", min_value=0.0, value=50000.0, step=1000.0)
        oldOrig   = st.number_input("Old Balance (Origin)", min_value=0.0, value=100000.0, step=1000.0)

    with c2:
        newOrig   = st.number_input("New Balance (Origin)", min_value=0.0, value=50000.0, step=1000.0)
        oldDest   = st.number_input("Old Balance (Destination)", min_value=0.0, value=0.0, step=1000.0)
        newDest   = st.number_input("New Balance (Destination)", min_value=0.0, value=50000.0, step=1000.0)

    submitted = st.form_submit_button("🔍 Predict Fraud", type="primary", use_container_width=True)

# ── Prediction ────────────────────────────────────────────────────
if submitted:
    input_df = pd.DataFrame([{
        'step': step,
        'type': t_type,
        'amount': amount,
        'oldbalanceOrg': oldOrig,
        'newbalanceOrig': newOrig,
        'oldbalanceDest': oldDest,
        'newbalanceDest': newDest
    }])

    try:
        with st.spinner("Analyzing transaction patterns..."):
            
            prediction, proba = make_prediction(input_df)
            probs = np.array(proba).flatten()
            proba_value = float(probs[1]) if len(probs) > 1 else float(probs[0])
            proba_pct = proba_value * 100

        st.markdown("---")
        st.markdown("### 🔎 Prediction Result")

        col_res, col_gauge = st.columns([1, 1])

        with col_res:
            if prediction == 1:
                st.error("🔴 **FRAUD DETECTED**")
                st.warning(f"""
**High Risk Transaction**
- Fraud Probability: **{proba_pct:.1f}%**
- Transaction Type: **{t_type}**
- Amount: **${amount:,.2f}**

This transaction shows patterns consistent with fraudulent activity. Immediate review recommended.
""")
            else:
                st.success("🟢 **Transaction is SAFE**")
                st.info(f"Fraud Probability: **{proba_pct:.1f}%** — No suspicious patterns detected.")

        with col_gauge:
            st.markdown('<div class="gauge-container">', unsafe_allow_html=True)
            st.markdown("**Fraud Probability Meter**")

            # Color logic
            if proba_pct < 30:
                bar_color = "#34a853" # Green
            elif proba_pct < 60:
                bar_color = "#fbbc04" # Yellow
            else:
                bar_color = "#ea4335" # Red

            st.markdown(f"""
            <div style="margin-top:12px">
                <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#666;">
                    <span>Safe (0%)</span><span>Danger (100%)</span>
                </div>
                <div style="background:#e0e0e0; border-radius:8px; height:28px; margin-top:6px; overflow:hidden;">
                    <div style="width:{proba_pct:.1f}%; background:{bar_color}; height:100%; border-radius:8px;
                                display:flex; align-items:center; justify-content:center;
                                color:white; font-weight:700; font-size:0.9rem; transition:width 0.5s;">
                        {proba_pct:.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Input Summary**")
            summary = pd.DataFrame({
                'Feature': ['Step', 'Type', 'Amount', 'Old Bal (Org)', 'New Bal (Org)', 'Old Bal (Dest)', 'New Bal (Dest)'],
                'Value': [step, t_type, f"${amount:,.2f}", f"${oldOrig:,.2f}", f"${newOrig:,.2f}", f"${oldDest:,.2f}", f"${newDest:,.2f}"]
            })
            st.dataframe(summary, hide_index=True, use_container_width=True)

    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بملف التوقع: {e}")