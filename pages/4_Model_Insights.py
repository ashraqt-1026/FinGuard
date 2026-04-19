import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_curve, auc, precision_recall_curve,
                             precision_score, recall_score, f1_score, roc_auc_score)
from Fraud_Detection_Model.src.model import make_prediction

st.set_page_config(page_title="Model Insights · FinGuard 360", page_icon="🧠", layout="wide")
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
def load_and_evaluate():
    # ── Fraud Model Data ───────────────────────────────────────────
    fraud_model = joblib.load("Fraud_Detection_Model/model/model.pkl")
    fraud_df    = pd.read_csv("Fraud_Detection_Model/fraud_sample.csv")
    
    Xf = fraud_df.drop(['isFraud'], axis=1)
    yf = fraud_df['isFraud']
    _, Xft, _, yft = train_test_split(Xf, yf, test_size=0.5, random_state=42, stratify=yf)
    
    yf_pred, yf_proba_full = make_prediction(Xft)
    yf_proba = yf_proba_full[:, 1] if yf_proba_full.ndim > 1 else yf_proba_full

    # ── Credit Model Data ──────────────────────────────────────────
    credit_model = joblib.load("Credit_risk_model/saved_models/credit_risk_model.pkl")
    credit_df    = pd.read_csv("Credit_risk_model/credit_risk_dataset.csv")
    
    credit_df['person_emp_length'] = credit_df['person_emp_length'].fillna(credit_df['person_emp_length'].median())
    credit_df['loan_int_rate'] = credit_df['loan_int_rate'].fillna(credit_df['loan_int_rate'].median())
    credit_df = credit_df[credit_df['person_age'] <= 100]
    credit_df = credit_df[credit_df['person_emp_length'] <= 60]
    credit_df.drop_duplicates(inplace=True)

    Xc = credit_df.drop('loan_status', axis=1)
    yc = credit_df['loan_status']
    _, Xct, _, yct = train_test_split(Xc, yc, test_size=0.2, random_state=42, stratify=yc)
    
    yc_pred  = credit_model.predict(Xct)
    yc_proba = credit_model.predict_proba(Xct)[:, 1]

    return (fraud_model, yft, yf_pred, yf_proba,
            credit_model, yct, yc_pred, yc_proba)

fraud_model, yft, yf_pred, yf_proba, credit_model, yct, yc_pred, yc_proba = load_and_evaluate()

st.markdown("# 🧠 Model Insights")
tab1, tab2 = st.tabs(["💳 Fraud Detection Model", "🏦 Credit Risk Model"])

# ─────────────────────────────────────────────────────────────────
# FRAUD TAB
# ─────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### 💳 Fraud Detection Model — Performance")

    col1, col2, col3 = st.columns(3)
    col1.metric("Precision (Fraud)", f"{precision_score(yft, yf_pred):.3f}")
    col2.metric("Recall (Fraud)", f"{recall_score(yft, yf_pred):.3f}")
    col3.metric("ROC-AUC", f"{roc_auc_score(yft, yf_proba):.4f}")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Confusion Matrix**")
        fig, ax = plt.subplots(figsize=(4, 3))
        cm = confusion_matrix(yft, yf_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['Normal','Fraud'], yticklabels=['Normal','Fraud'])
        ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with r2:
        st.markdown("**ROC Curve**")
        fig, ax = plt.subplots(figsize=(4, 3))
        fpr, tpr, _ = roc_curve(yft, yf_proba)
        ax.plot(fpr, tpr, color='#1a73e8', lw=2, label=f'AUC = {auc(fpr, tpr):.4f}')
        ax.plot([0,1],[0,1],'--', color='gray', lw=1)
        ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
        ax.legend(loc='lower right')
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown("**Top 10 Feature Importances**")
    try:
        preprocessor = joblib.load("Fraud_Detection_Model/preprocessor.pkl")
        feature_names = preprocessor.get_feature_names_out()
        importances = fraud_model.feature_importances_
        fi_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
        fi_df = fi_df.sort_values('Importance', ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(fi_df['Feature'][::-1], fi_df['Importance'][::-1], color='#1a73e8')
        ax.set_title("Top 10 Feature Importances — Fraud")
        plt.tight_layout()
        st.pyplot(fig); plt.close()
    except:
        st.info("Feature importance visualization is unavailable for this configuration.")

# ─────────────────────────────────────────────────────────────────
# CREDIT TAB
# ─────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### 🏦 Credit Risk Model — Performance")

    col1, col2, col3 = st.columns(3)
    col1.metric("F1-Score (Default)", f"{f1_score(yct, yc_pred):.3f}")
    col2.metric("Recall (Default)", f"{recall_score(yct, yc_pred):.3f}")
    col3.metric("ROC-AUC", f"{roc_auc_score(yct, yc_proba):.4f}")

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Confusion Matrix**")
        fig, ax = plt.subplots(figsize=(4, 3))
        cm = confusion_matrix(yct, yc_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', ax=ax,
                    xticklabels=['No Default','Default'], yticklabels=['No Default','Default'])
        ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with r2:
        st.markdown("**ROC Curve**")
        fig, ax = plt.subplots(figsize=(4, 3))
        fpr, tpr, _ = roc_curve(yct, yc_proba)
        ax.plot(fpr, tpr, color='#ea4335', lw=2, label=f'AUC = {auc(fpr, tpr):.4f}')
        ax.plot([0,1],[0,1],'--', color='gray', lw=1)
        ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
        ax.legend(loc='lower right')
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown("**Top 10 Feature Importances**")
    try:
        # استخراج أسماء الميزات من الـ Pipeline
        prep = credit_model.named_steps['preprocessor']
        clf = credit_model.named_steps['classifier']
        
        num_names = prep.transformers_[0][2]
        cat_transformer = prep.transformers_[1][1]
        cat_features = prep.transformers_[1][2]
        cat_names = list(cat_transformer.get_feature_names_out(cat_features))
        
        all_features = num_names + cat_names
        fi_df = pd.DataFrame({'Feature': all_features, 'Importance': clf.feature_importances_})
        fi_df = fi_df.sort_values('Importance', ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(fi_df['Feature'][::-1], fi_df['Importance'][::-1], color='#ea4335')
        ax.set_title("Top 10 Feature Importances — Credit Risk")
        plt.tight_layout()
        st.pyplot(fig); plt.close()
    except:
        st.info("Feature importance visualization is unavailable for this configuration.")