import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Data Dashboard · FinGuard 360", page_icon="📊", layout="wide")
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

@st.cache_data
def load_data():
    fraud_df  = pd.read_csv("Fraud_Detection_Model/fraud_sample.csv")
    credit_df = pd.read_csv("Credit_risk_model/credit_risk_dataset.csv")
    
    credit_df['person_emp_length'] = credit_df['person_emp_length'].fillna(credit_df['person_emp_length'].median())
    credit_df['loan_int_rate'] = credit_df['loan_int_rate'].fillna(credit_df['loan_int_rate'].median())
    credit_df = credit_df[credit_df['person_age'] <= 100]
    credit_df = credit_df[credit_df['person_emp_length'] <= 60]
    credit_df.drop_duplicates(inplace=True)
    return fraud_df, credit_df

fraud_df, credit_df = load_data()

st.markdown("# 📊 Data Dashboard")

# ── KPIs ─────────────────────────────────────────────────────────
st.markdown("### 📌 Key Metrics")
k1, k2, k3, k4 = st.columns(4)
k1.metric("💳 Fraud Rate", f"{fraud_df['isFraud'].mean()*100:.2f}%")
k2.metric("⚠️ Default Rate", f"{credit_df['loan_status'].mean()*100:.1f}%")
k3.metric("💰 Avg Income", f"${credit_df['person_income'].mean():,.0f}")
k4.metric("💵 Avg Transaction", f"${fraud_df['amount'].mean():,.0f}")

st.markdown("---")

# ── Fraud Visuals ─────────────────────────────────────────────────
st.markdown("## 💳 Fraud Detection Dataset")
f1, f2 = st.columns(2)

with f1:
    st.markdown("**Fraud vs Normal Distribution**")
    fig, ax = plt.subplots(figsize=(5, 4))
    counts = fraud_df['isFraud'].value_counts()
    ax.pie(counts, labels=['Normal', 'Fraud'], autopct='%1.1f%%',
           colors=['#34a853', '#ea4335'], startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax.set_title("Fraud vs Normal", fontsize=13, fontweight='bold')
    st.pyplot(fig)
    plt.close()

with f2:
    st.markdown("**Fraud Count by Transaction Type**")
    fig, ax = plt.subplots(figsize=(5, 4))
    fraud_by_type = fraud_df.groupby('type')['isFraud'].sum().sort_values(ascending=False)
    bars = ax.bar(fraud_by_type.index, fraud_by_type.values,
                  color=['#ea4335' if t in ['TRANSFER','CASH_OUT'] else '#1a73e8' for t in fraud_by_type.index])
    ax.set_title("Fraud Count by Type", fontsize=13, fontweight='bold')
    ax.set_xlabel("Transaction Type")
    ax.set_ylabel("Fraud Count")
    plt.xticks(rotation=15)
    st.pyplot(fig)
    plt.close()

f3, f4 = st.columns(2)

with f3:
    st.markdown("**Transaction Amount Distribution**")
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist(fraud_df[fraud_df['amount'] < 1_000_000]['amount'],
            bins=50, color='#1a73e8', alpha=0.7, edgecolor='white')
    ax.set_title("Amount Distribution (<$1M)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Amount ($)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close()

with f4:
    st.markdown("**Correlation Heatmap (Fraud Features)**")
    fig, ax = plt.subplots(figsize=(5, 4))
    num_fraud = fraud_df[['amount','oldbalanceOrg',
                           'oldbalanceDest','isFraud']]
    sns.heatmap(num_fraud.corr(), annot=True, fmt=".2f", cmap='coolwarm',
                linewidths=0.5, ax=ax, annot_kws={"size": 8})
    ax.set_title("Feature Correlation", fontsize=13, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Credit Visuals ────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🏦 Credit Risk Dataset")
c1, c2 = st.columns(2)

with c1:
    st.markdown("**Income Distribution**")
    fig, ax = plt.subplots(figsize=(5, 4))
    clipped = credit_df[credit_df['person_income'] < 300000]['person_income']
    ax.hist(clipped, bins=50, color='#1a73e8', alpha=0.7, edgecolor='white')
    ax.set_title("Annual Income Distribution", fontsize=13, fontweight='bold')
    ax.set_xlabel("Income ($)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close()

with c2:
    st.markdown("**Loan Amount Distribution**")
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist(credit_df['loan_amnt'], bins=50, color='#fbbc04', alpha=0.8, edgecolor='white')
    ax.set_title("Loan Amount Distribution", fontsize=13, fontweight='bold')
    ax.set_xlabel("Loan Amount ($)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close()

c3, c4 = st.columns(2)

with c3:
    st.markdown("**Default Rate (Loan Status)**")
    fig, ax = plt.subplots(figsize=(5, 4))
    status_counts = credit_df['loan_status'].value_counts()
    ax.pie(status_counts, labels=['No Default', 'Default'], autopct='%1.1f%%',
           colors=['#34a853', '#ea4335'], startangle=90,
           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax.set_title("Loan Status Distribution", fontsize=13, fontweight='bold')
    st.pyplot(fig)
    plt.close()

with c4:
    st.markdown("**Income vs Loan Amount**")
    fig, ax = plt.subplots(figsize=(5, 4))
    sample = credit_df.sample(min(2000, len(credit_df)), random_state=42)
    colors = sample['loan_status'].map({0: '#34a853', 1: '#ea4335'})
    ax.scatter(sample['person_income'], sample['loan_amnt'],
                c=colors, alpha=0.4, s=15)
    ax.set_xlim(0, 300000)
    ax.set_title("Income vs Loan Amount", fontsize=13, fontweight='bold')
    ax.set_xlabel("Income ($)")
    ax.set_ylabel("Loan Amount ($)")
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#34a853', label='No Default'),
                       Patch(facecolor='#ea4335', label='Default')]
    ax.legend(handles=legend_elements, loc='upper right')
    st.pyplot(fig)
    plt.close()