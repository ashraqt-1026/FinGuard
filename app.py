import streamlit as st

st.set_page_config(
    page_title="FinGuard 360",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Clean Global Styling ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* Background */
.stApp { background-color: #F0F4F8; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1A2B4A;
}
[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] a:hover {
    color: #63B3ED !important;
}

/* Typography */
h1 { color: #1A2B4A !important; font-size: 2rem !important; font-weight: 700 !important; }
h2 { color: #1A2B4A !important; font-weight: 600 !important; }
h3 { color: #2D3748 !important; font-weight: 600 !important; }
p, li { color: #2D3748 !important; }

/* Metric cards */
div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E0;
    padding: 20px 24px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
div[data-testid="metric-container"] label {
    color: #718096 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1A2B4A !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button {
    background-color: #2B6CB0;
    color: white !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #2C5282;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ FinGuard 360")
    st.markdown("**Enterprise AI Risk Platform**")
    st.markdown("---")
    st.markdown("#### Navigation")
    st.markdown("- 🏠 **Home** ← You are here")
    st.markdown("- 💳 Fraud Detection")
    st.markdown("- 🏦 Credit Risk")
    st.markdown("- 📊 Data Dashboard")
    st.markdown("- 🧠 Model Insights")
    st.markdown("- 🧑‍🏫 Discussion")
    st.markdown("---")
    st.markdown("**Version:** 2.0.0")
    st.markdown("**Status:** 🟢 All Systems Online")

# ── Main Content ─────────────────────────────────────────────────────────────
st.markdown("# 🛡️ FinGuard 360 — Command Center")
st.markdown("#### Monitor, analyze, and mitigate financial risks in real-time.")
st.markdown("---")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions",  "1,200,000",  "+5.2%")
col2.metric("Fraud Rate",          "1.85%",      "-0.12%")
col3.metric("Avg Credit Risk",     "Low–Mid",    "Stable", delta_color="off")
col4.metric("Approval Rate",       "74.2%",      "+1.5%")

st.markdown("<br>", unsafe_allow_html=True)

# Module Cards
st.markdown("### 🚀 Active Modules")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div style="background:#FFFFFF; padding:24px; border-radius:12px;
                border-left:5px solid #E53E3E; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <h3 style="color:#1A2B4A; margin-top:0;">💳 Fraud Detection Engine</h3>
        <p style="color:#4A5568;">Real-time anomaly detection for transactional data using XGBoost.
        Detects fraudulent TRANSFER and CASH_OUT patterns with 99%+ precision.</p>
        <span style="background:#FED7D7; color:#C53030; padding:4px 10px;
                     border-radius:20px; font-size:0.8rem; font-weight:600;">LIVE</span>
    </div><br>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Fraud_Detection.py", label="Launch Fraud Module →")

with col_b:
    st.markdown("""
    <div style="background:#FFFFFF; padding:24px; border-radius:12px;
                border-left:5px solid #3182CE; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <h3 style="color:#1A2B4A; margin-top:0;">🏦 Credit Risk Engine</h3>
        <p style="color:#4A5568;">Advanced applicant profiling and loan default prediction.
        92% accuracy with ROC-AUC of 0.95 on real credit data.</p>
        <span style="background:#BEE3F8; color:#2C5282; padding:4px 10px;
                     border-radius:20px; font-size:0.8rem; font-weight:600;">LIVE</span>
    </div><br>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Credit_Risk.py", label="Launch Credit Module →", icon="📊")

st.markdown("<br>", unsafe_allow_html=True)

# Info Row
st.markdown("### 📋 System Overview")
col_c, col_d, col_e = st.columns(3)
with col_c:
    st.markdown("""
    <div style="background:#FFFFFF; padding:20px; border-radius:12px; text-align:center;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <h2 style="color:#38A169; margin:0;">92%</h2>
        <p style="color:#718096; margin:4px 0 0 0;">Credit Model Accuracy</p>
    </div>""", unsafe_allow_html=True)
with col_d:
    st.markdown("""
    <div style="background:#FFFFFF; padding:20px; border-radius:12px; text-align:center;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <h2 style="color:#3182CE; margin:0;">0.95</h2>
        <p style="color:#718096; margin:4px 0 0 0;">ROC-AUC Score</p>
    </div>""", unsafe_allow_html=True)
with col_e:
    st.markdown("""
    <div style="background:#FFFFFF; padding:20px; border-radius:12px; text-align:center;
                box-shadow:0 2px 8px rgba(0,0,0,0.06);">
        <h2 style="color:#D69E2E; margin:0;">28,500</h2>
        <p style="color:#718096; margin:4px 0 0 0;">Training Samples</p>
    </div>""", unsafe_allow_html=True)