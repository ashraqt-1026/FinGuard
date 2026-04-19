import os
import joblib
import pandas as pd

from Fraud_Detection_Model.preprocessing import preprocess_data
model = joblib.load('Fraud_Detection_Model/model/model.pkl')

def make_prediction(df: pd.DataFrame):
    processed_data = preprocess_data(df)
    prediction = model.predict(processed_data)
    
    probabilities = model.predict_proba(processed_data)
    
    return prediction, probabilities