import streamlit as st

st.set_page_config(page_title="Discussion · FinGuard 360", page_icon="🧑‍🏫", layout="wide")
st.markdown("""<style>.main { background-color: #f8f9fa; }
.section-box { background: white; border-radius: 12px; padding: 20px;
               box-shadow: 0 2px 8px rgba(0,0,0,0.07); margin-bottom: 16px; }
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=60)
    st.markdown("## 🛡️ FinGuard 360")
    st.markdown("---")
    st.page_link("app.py",                              label="🏠 Home Dashboard")
    st.page_link("pages/1_Fraud_Detection.py",          label="💳 Fraud Detection")
    st.page_link("pages/2_Credit_Risk.py",              label="🏦 Credit Risk")
    st.page_link("pages/3_Data_Dashboard.py",           label="📊 Data Dashboard")
    st.page_link("pages/4_Model_Insights.py",           label="🧠 Model Insights")
    st.page_link("pages/5_Discussion.py",               label="🧑‍🏫 Discussion")

st.markdown("# 🧑‍🏫 System Discussion")
st.markdown("Technical overview, design decisions, limitations, and future roadmap.")
st.markdown("---")

# ── System Architecture ───────────────────────────────────────────
st.markdown("## 🏗️ System Architecture")

st.markdown("""
```
User Input (Streamlit UI)
        │
        ├──► 💳 Fraud Detection Page ──► fraud_model.pkl (XGBoost)
        │         │
        │         └──► Fraud Probability → 🔴 Alert / 🟢 Safe
        │
        └──► 🏦 Credit Risk Page ──────► credit_risk_model.pkl (XGBoost)
                  │
                  └──► Default Probability → ✅ Approve / ❌ Reject

📊 Data Dashboard ──► @st.cache_data ──► Preloaded DataFrames (Matplotlib + Seaborn)
🧠 Model Insights ──► Cached evaluation ──► ROC, CM, Feature Importance
```
""")

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("""
**Data Flow:**
1. User fills form → Streamlit captures raw input values
2. Input assembled into a `pandas DataFrame` matching training column order
3. `Pipeline.predict_proba()` runs: Scaler → OneHotEncoder → XGBClassifier
4. Probability score mapped to risk tier and decision
5. Result displayed with visual gauge
""")
st.markdown('</div>', unsafe_allow_html=True)

# ── Why 2 Models ──────────────────────────────────────────────────
st.markdown("## 🤔 Why Two Separate Models?")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.07); color:#1a1a1a;">
    <h4 style="color:#ea4335; margin-top:0;">💳 Fraud Detection Model</h4>
    <ul style="color:#333; padding-left:18px; line-height:1.8;">
        <li><b>Target:</b> Individual transaction anomaly</li>
        <li><b>Data:</b> Real-time transaction stream (PaySim)</li>
        <li><b>Features:</b> Amount, balance changes, error balance</li>
        <li><b>Key signal:</b> Balance discrepancies after transaction</li>
        <li><b>Decision speed:</b> Milliseconds (real-time)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:white; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.07); color:#1a1a1a;">
    <h4 style="color:#1a73e8; margin-top:0;">🏦 Credit Risk Model</h4>
    <ul style="color:#333; padding-left:18px; line-height:1.8;">
        <li><b>Target:</b> Loan applicant default probability</li>
        <li><b>Data:</b> Static applicant profile (Credit Risk dataset)</li>
        <li><b>Features:</b> Income, age, loan grade, employment, credit history</li>
        <li><b>Key signal:</b> Loan grade + loan % of income</li>
        <li><b>Decision speed:</b> Seconds (pre-approval workflow)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ── Limitations ───────────────────────────────────────────────────
st.markdown("## ⚠️ System Limitations")
st.warning("""
**Known Limitations:**
1. **Different Data Sources** — Fraud model uses synthetic PaySim data; real-world fraud patterns may differ significantly.
2. **No Unified Schema** — The two models share no common features, preventing cross-model scoring.
3. **Static Models** — Models are not retrained on new data (no online learning).
4. **No Time Features** — Transaction timestamp/sequence not used in the fraud model.
5. **Threshold Fixed** — Fraud/risk thresholds (30%, 60%) are hardcoded, not optimized per business cost.
""")

# ── Future Work ───────────────────────────────────────────────────
st.markdown("## 🚀 Future Work")
st.success("""
**Planned Improvements:**
1. 🔗 **Unified Scoring Engine** — Single risk score combining fraud + credit signals per customer.
2. 🔍 **SHAP Explainability** — Per-prediction feature contribution breakdown for model transparency.
3. 🌐 **REST API Deployment** — FastAPI + Docker containerization for production deployment.
4. 📈 **Model Monitoring** — Drift detection with Evidently AI or WhyLabs.
5. ⚡ **Real-time Streaming** — Kafka integration for live transaction scoring.
6. 🧪 **A/B Testing Framework** — Champion/Challenger model comparison in production.
""")

# ── Tech Stack ────────────────────────────────────────────────────
st.markdown("## 🛠️ Tech Stack")
import pandas as pd
tech_data = {
    'Component':   ['ML Framework', 'Model Type', 'Imbalance Handling', 'Deployment', 'Visualization', 'Data Processing'],
    'Technology':  ['XGBoost 2.x', 'Gradient Boosted Trees', 'scale_pos_weight + stratified split', 'Streamlit', 'Matplotlib + Seaborn', 'Pandas + Scikit-learn Pipeline'],
    'Purpose':     ['Core ML engine', 'Handles mixed features, non-linear patterns', 'Class imbalance correction', 'Interactive web UI', 'Charts and heatmaps', 'Preprocessing + feature engineering']
}
tech_df = pd.DataFrame(tech_data)
st.dataframe(tech_df, hide_index=True, use_container_width=True)
