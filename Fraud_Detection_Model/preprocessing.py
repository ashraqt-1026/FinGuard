import pandas as pd
import joblib

preprocessor = joblib.load("Fraud_Detection_Model/preprocessor.pkl")

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function takes raw dataframe and returns cleaned dataframe
    """
    if(df['type'].isnull().sum() > 0):
        df.fillna("CASH_OUT")
    df.fillna(0)
    df_final = preprocessor.transform(df)

    return df_final