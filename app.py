import streamlit as st

st.set_page_config(
    page_title="FinGuard 360",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Clean Dark Theme Styling ────────────────────────────────────────────────
st.markdown("""
<style>
/* Background - Dark */
.stApp { background-color: #0E1117; }

/* Sidebar - Darker */
[data-testid="stSidebar"] {
    background-color: #05070A;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Typography - White for Readability on Dark */
h1, h2, h3, p, li, label, span { color: #FFFFFF !important; }

/* Metric cards - Dark with Border */
div[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

/* Buttons */
.stButton > button {
    background-color: #1A73E8;
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #1557B0;
    border: none;
}

/* Links and dividers */
hr { border-color: #30363D !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ FinGuard 360")
    st.markdown("---")
    st.markdown("#### Navigation")
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_Fraud_Detection.py", label="💳 Fraud Detection")
    st.page_link("pages/2_Credit_Risk.py", label="🏦 Credit Risk")
    st.page_link("pages/3_Data_Dashboard.py", label="📊 Data Dashboard")
    st.page_link("pages/4_Model_Insights.py", label="🧠 Model Insights")
    st.page_link("pages/5_Discussion.py", label="🧑‍🏫 Discussion")
    st.markdown("---")
    st.markdown("**Status:** 🟢 Online")

# ── Main Content ─────────────────────────────────────────────────────────────
st.markdown("# 🛡️ FinGuard 360 — Command Center")
st.markdown("Monitor, analyze, and mitigate financial risks in real-time.")
st.markdown("---")

# KPIs Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", "1,200,000", "+5.2%")
col2.metric("Fraud Rate", "1.85%", "-0.12%")
col3.metric("Avg Credit Risk", "Low–Mid", "Stable", delta_color="off")
col4.metric("Approval Rate", "74.2%", "+1.5%")

st.markdown("<br>", unsafe_allow_html=True)

# Module Cards
st.markdown("### 🚀 Active Modules")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div style="background:#161B22; padding:24px; border-radius:12px;
                border: 1px solid #30363D; border-left:5px solid #E53E3E;">
        <h3 style="margin-top:0; color:#FFFFFF;">💳 Fraud Detection Engine</h3>
        <p style="color:#C9D1D9;">Real-time anomaly detection for transactional data using XGBoost.</p>
        <span style="background:#442323; color:#FF6B6B; padding:4px 10px;
                     border-radius:20px; font-size:0.8rem; font-weight:600;">LIVE</span>
    </div><br>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Fraud_Detection.py", label="Launch Fraud Module →")

with col_b:
    st.markdown("""
    <div style="background:#161B22; padding:24px; border-radius:12px;
                border: 1px solid #30363D; border-left:5px solid #1A73E8;">
        <h3 style="margin-top:0; color:#FFFFFF;">🏦 Credit Risk Engine</h3>
        <p style="color:#C9D1D9;">Advanced applicant profiling and loan default prediction.</p>
        <span style="background:#1C2C42; color:#58A6FF; padding:4px 10px;
                     border-radius:20px; font-size:0.8rem; font-weight:600;">LIVE</span>
    </div><br>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Credit_Risk.py", label="Launch Credit Module →")