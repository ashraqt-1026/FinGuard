# 🛡️ FinGuard 360

> **AI-Powered Enterprise Financial Risk Platform**  
> Real-time fraud detection and intelligent credit risk assessment — unified in a single interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189AB4?style=flat)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## Overview

FinGuard 360 is a multi-page Streamlit web application that provides a unified command center for financial risk management. It addresses two critical threats in modern banking:

- **Transactional Fraud** — Real-time anomaly detection on payment transactions using XGBoost.
- **Credit Risk & Defaults** — Advanced applicant profiling and loan default prediction with probability output.

Both modules are live and accessible through an interactive dark-themed dashboard with real-time KPI monitoring.

---

## Screenshots

> _Add screenshots of your dashboard, fraud detection, and credit risk pages here._

---

## App Structure

```
FinGuard/
├── app.py                        # Home — Command Center (KPIs + module launcher)
├── pages/
│   ├── 1_Fraud_Detection.py      # 💳 Fraud Detection Engine
│   ├── 2_Credit_Risk.py          # 🏦 Credit Risk Assessment Engine
│   ├── 3_Data_Dashboard.py       # 📊 Data Dashboard
│   ├── 4_Model_Insights.py       # 🧠 Model Insights & Feature Importance
│   └── 5_Discussion.py           # 🧑‍🏫 Discussion & Methodology
└── requirements.txt
```

---

## Features

### 🏠 Home — Command Center
- Live KPI tiles: Total Transactions, Fraud Rate, Avg Credit Risk, Approval Rate
- Module launcher cards for Fraud Detection and Credit Risk engines
- Sidebar navigation across all pages
- Dark-themed UI with custom CSS styling

### 💳 Fraud Detection Engine
- XGBoost classifier trained on transactional data
- Real-time anomaly detection on payment transactions
- Binary fraud flag with confidence score output

### 🏦 Credit Risk Engine
- Advanced applicant profiling and loan default prediction
- Continuous risk percentage + Low / Medium / High tier classification
- Handles class imbalance via `scale_pos_weight` and stratified splits

### 📊 Data Dashboard
- Visual exploration of transaction and applicant datasets
- Distribution plots, correlation heatmaps, class balance charts

### 🧠 Model Insights
- Feature importance visualization for both ML models
- Explainable AI — understand *why* each prediction is made

### 🧑‍🏫 Discussion
- Methodology notes, model rationale, and academic context

---

## Tech Stack

| Category | Library |
|---|---|
| **Web App** | `streamlit` |
| **Machine Learning** | `xgboost`, `scikit-learn` |
| **Data Engineering** | `pandas`, `numpy` |
| **Encoding** | `category_encoders` |
| **Model Persistence** | `joblib` |
| **Visualization** | `matplotlib`, `seaborn` |

---

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/ashraqt-1026/FinGuard.git
cd FinGuard

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## Usage

1. **Home** — Start at the Command Center to see live KPIs and navigate to modules.
2. **Fraud Detection** — Input transaction details to get a real-time fraud flag and confidence score.
3. **Credit Risk** — Enter applicant details to receive a risk percentage and tier (Low / Medium / High).
4. **Data Dashboard** — Explore the underlying datasets visually.
5. **Model Insights** — Inspect feature importances to understand model behavior.
6. **Discussion** — Review methodology and model design decisions.

---

## Dependencies

```
streamlit
pandas
numpy
scikit-learn
joblib
matplotlib
seaborn
xgboost
category_encoders
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## Dashboard KPIs

| Metric | Value | Trend |
|---|---|---|
| Total Transactions | 1,200,000 | +5.2% |
| Fraud Rate | 1.85% | -0.12% |
| Avg Credit Risk | Low–Mid | Stable |
| Approval Rate | 74.2% | +1.5% |

---

## Roadmap

- [x] Fraud Detection Engine (XGBoost)
- [x] Credit Risk Engine (XGBoost)
- [x] Interactive Streamlit dashboard
- [x] Feature importance visualization
- [ ] FastAPI REST inference endpoint
- [ ] Unified ML scoring engine
- [ ] Real-time streaming with Apache Kafka
- [ ] SHAP value explainability layer
- [ ] Model drift detection & monitoring

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add: your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <strong>FinGuard 360</strong> · Built with Streamlit & XGBoost · 🛡️ Status: Online
</div>