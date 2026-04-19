import streamlit as st
import pandas as pd

st.set_page_config(page_title="Discussion · FinGuard 360", page_icon="🧑‍🏫", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .section-box { 
        background: white; 
        border-radius: 12px; 
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07); 
        margin-bottom: 16px; 
        color: #1a1a1a;
    }
    .model-card {
        background: white; 
        border-radius: 12px; 
        padding: 20px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.07); 
        color: #1a1a1a;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

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

st.markdown("# 🧑‍🏫 System Discussion")
st.markdown("Technical overview, design decisions, limitations, and future roadmap.")
st.markdown("---")

# ── System Architecture ───────────────────────────────────────────
st.markdown("## 🏗️ System Architecture")

st.code("""
User Input (Streamlit UI)
        │
        ├──► 💳 Fraud Detection Page ──► fraud_model.pkl (XGBoost)
        │         │
        │         └──► Fraud Probability → 🔴 Alert / 🟢 Safe
        │
        └──► 🏦 Credit Risk Page ──────► credit_risk_model.pkl (XGBoost)
                  │
                  └──► Default Probability → ✅ Approve / ❌ Reject

📊 Data Dashboard ──► Cached DataFrames (Matplotlib + Seaborn)
🧠 Model Insights ──► Cached evaluation ──► ROC, CM, Feature Importance
""", language="text")

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("""
**Data Flow:**
1. **Input:** User fills form → Streamlit captures raw input values.
2. **Assembly:** Input assembled into a `pandas DataFrame` matching training column order.
3. **Processing:** `Pipeline.predict_proba()` runs: Scaler → OneHotEncoder → XGBClassifier.
4. **Scoring:** Probability score mapped to risk tier and decision.
5. **Output:** Result displayed with interactive visual gauges.
""")
st.markdown('</div>', unsafe_allow_html=True)

# ── Why 2 Models ──────────────────────────────────────────────────
st.markdown("## 🤔 Why Two Separate Models?")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="model-card">
    <h4 style="color:#ea4335; margin-top:0;">💳 Fraud Detection Model</h4>
    <ul style="color:#333; padding-left:18px; line-height:1.8;">
        <li><b>Target:</b> Individual transaction anomaly.</li>
        <li><b>Data:</b> Real-time transaction stream (PaySim).</li>
        <li><b>Features:</b> Amount, balance changes, error balance.</li>
        <li><b>Key signal:</b> Balance discrepancies after transaction.</li>
        <li><b>Decision speed:</b> Milliseconds (real-time).</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="model-card">
    <h4 style="color:#1a73e8; margin-top:0;">🏦 Credit Risk Model</h4>
    <ul style="color:#333; padding-left:18px; line-height:1.8;">
        <li><b>Target:</b> Loan applicant default probability.</li>
        <li><b>Data:</b> Static applicant profile (Credit Risk dataset).</li>
        <li><b>Features:</b> Income, age, loan grade, employment history.</li>
        <li><b>Key signal:</b> Loan grade + loan % of income.</li>
        <li><b>Decision speed:</b> Seconds (pre-approval workflow).</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ── Limitations ───────────────────────────────────────────────────
st.markdown("## ⚠️ System Limitations")
st.warning("""
1. **Synthetic Data Bias** — Fraud model uses PaySim data; real-world patterns may evolve differently.
2. **Disconnected Schemas** — Models share no common features, preventing a unified customer risk profile.
3. **Static Deployment** — Models require manual retraining (no automated online learning).
4. **Hardcoded Thresholds** — Risk boundaries (30%, 60%) are fixed and may need business tuning.
""")

# ── Future Work ───────────────────────────────────────────────────
st.markdown("## 🚀 Future Work")
st.success("""
1. 🔗 **Unified Scoring** — Single risk engine combining fraud + credit signals per user.
2. 🔍 **Explainable AI (SHAP)** — Visual breakdown of why a specific decision was made.
3. 🌐 **API Integration** — FastAPI + Docker for external system consumption.
4. 📈 **Monitoring** — Drift detection to alert when data patterns change over time.
5. ⚡ **Streaming** — Kafka integration for processing millions of live transactions.
""")

# ── Tech Stack ────────────────────────────────────────────────────
st.markdown("## 🛠️ Tech Stack")
tech_data = {
    'Component': ['ML Framework', 'Model Type', 'Imbalance Handling', 'Deployment', 'Visualization', 'Data Processing'],
    'Technology': ['XGBoost 2.x', 'Gradient Boosted Trees', 'scale_pos_weight + Stratified Split', 'Streamlit', 'Matplotlib + Seaborn', 'Scikit-learn Pipelines'],
    'Purpose': ['Core ML engine', 'Handles non-linear patterns', 'Class imbalance correction', 'Interactive web UI', 'Analytical charts', 'Automated feature engineering']
}
tech_df = pd.DataFrame(tech_data)
st.table(tech_df)