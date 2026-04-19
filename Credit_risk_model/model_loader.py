import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models")
DATA_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credit_risk_dataset.csv")

def _train_credit():
    df = pd.read_csv(DATA_PATH)
    df = df[df['person_emp_length'] < 60].dropna()
    df.drop_duplicates(inplace=True)

    cat_cols = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
    le_dict  = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le

    X = df.drop('loan_status', axis=1)
    y = df['loan_status']
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = XGBClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.1,
        scale_pos_weight=(y_train==0).sum() / (y_train==1).sum(),
        random_state=42, eval_metric='logloss'
    )
    model.fit(X_train, y_train)

    bundle = {'model': model, 'feature_names': list(X.columns), 'label_encoders': le_dict}
    joblib.dump(bundle, os.path.join(MODELS_DIR, "credit_model.pkl"))
    return bundle

def _train_fraud():
    np.random.seed(42)
    n = 28500
    amounts      = np.random.exponential(scale=500, size=n)
    old_balances = np.random.uniform(0, 50000, size=n)
    new_balances = np.clip(old_balances - amounts * np.random.uniform(0.5, 1.5, size=n), 0, None)
    type_encoded = np.random.randint(0, 4, size=n)
    composite    = (old_balances - new_balances) * 0.5 + amounts * 0.5
    labels       = (composite > np.percentile(composite, 98)).astype(int)

    X = np.column_stack([amounts, type_encoded, old_balances, new_balances])
    X_train, _, y_train, _ = train_test_split(X, labels, test_size=0.2, random_state=42, stratify=labels)

    model = XGBClassifier(
        n_estimators=200,
        scale_pos_weight=(y_train==0).sum() / max((y_train==1).sum(), 1),
        random_state=42, eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    joblib.dump(model, os.path.join(MODELS_DIR, "fraud_model.pkl"))
    return model

def load_credit_model():
    """Load credit model — trains automatically if not found."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, "credit_model.pkl")
    if not os.path.exists(path):
        _train_credit()
    return joblib.load(path)

def load_fraud_model():
    """Load fraud model — trains automatically if not found."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    path = os.path.join(MODELS_DIR, "fraud_model.pkl")
    if not os.path.exists(path):
        _train_fraud()
    return joblib.load(path)