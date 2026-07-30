#  Intelligent Log Analytics & Anomaly Detection Platform

> AI-powered log analysis and anomaly detection for Hadoop Distributed File System (HDFS) execution logs using Machine Learning, Explainable AI (SHAP), and an interactive Streamlit dashboard.

---

##  Project Overview

The **Intelligent Log Analytics & Anomaly Detection Platform** is an interactive web application that analyzes HDFS execution logs to identify anomalous execution traces and provide meaningful insights into their causes.

The platform leverages a **Random Forest Classifier** trained on historical HDFS logs to classify execution traces as **Normal** or **Anomalous**. To improve transparency, the predictions are explained using **SHAP (SHapley Additive Explanations)**, allowing users to understand which events contributed most to a model's decision.

Beyond anomaly detection, the platform includes rich visual analytics, failure monitoring, AI-assisted explanations, root cause analysis, and actionable recommendations through an easy-to-use Streamlit dashboard.

---

#  Key Features

- Interactive analytics dashboard
- Machine Learning based anomaly detection
- Explainable AI using SHAP
- Rich data visualizations using Plotly
- Alert monitoring dashboard
- Root cause analysis
- Actionable recommendations
- Downloadable analytics reports
- Upload and analyze new datasets

---

# System Architecture

```
                    HDFS Event Logs
                           │
                           ▼
                  Data Preprocessing
                           │
                           ▼
             Feature Engineering (E1-E29)
                           │
                           ▼
              Random Forest Classifier
                           │
          ┌────────────────┴───────────────┐
          ▼                                ▼
  Prediction (Normal/Anomaly)         SHAP Explainability
          │                                │
          └──────────────┬─────────────────┘
                         ▼
             Streamlit Interactive Dashboard
                         │
                         ▼
      Visualizations • Reports • Recommendations
```

---

# Machine Learning Pipeline

### Dataset

The model is trained using the **HDFS Event Occurrence Matrix** dataset.

Each execution block contains:

- Block ID
- Event occurrence counts (E1–E29)
- Failure Type
- Success / Fail Label

Each row represents **one execution block** in Hadoop.

---

### Feature Set

The Random Forest model is trained using **29 numerical event occurrence features**.

```
E1
E2
...
E29
```

Target Variable

```
Success → 0
Fail → 1
```

---

### Model

Algorithm:

- Random Forest Classifier

Training-Test Split:

- 80% Training
- 20% Testing

Saved model:

```
saved_models/random_forest.pkl
```

---

# Explainable AI (SHAP)

The project uses **SHAP (SHapley Additive Explanations)** to interpret the predictions made by the Random Forest model.

For every execution trace:

- SHAP computes the contribution of every feature (E1–E29).
- Features with the highest absolute SHAP values are identified.
- These features are presented as the primary reasons behind the model's prediction.
- The insights page further maps these important events to likely causes and recommended corrective actions.

This enables users to understand **why** the model predicted an anomaly rather than treating the model as a black box.

---
# Dashboard Overview

## Home

- Project introduction
- Upload HDFS dataset
- Navigation to all modules

---

## Log Overview

Provides an overall summary of uploaded logs.

Features:

- Total Logs
- Normal Logs
- Anomalous Logs
- Anomaly Rate
- Success vs Failure Distribution
- Top Anomaly-Associated Events
- Top Event Templates
- Event Frequency Table

---

## Model Analytics

### Dataset Review

- Event Occurrence Heatmap
- Failure Type Analysis
- Dataset Preview

### Block Analysis

Users can inspect any execution block individually.

Displays:

- Actual Label
- Predicted Label
- Prediction Confidence
- Feature Importance
- Event Analysis
- Model Explanation

### Report

Generates a downloadable analytics report for the selected execution block.

---

## Anomaly Detection

Predicts whether an execution block is anomalous.

Displays:

- Prediction
- Actual Label
- Confidence Score
- Severity Level
- Anomaly Probability
- Top Event Occurrences
- Complete Event Pattern

---

## Alerts & Failures Dashboard

Provides operational monitoring.

Features:

- Total Alerts
- Alert Rate
- Healthy Logs
- Failure Type Distribution
- Recent Anomalous Blocks
- Export Alert Report

---

## Actionable Insights

Provides explainable predictions.

Displays:

- SHAP-based model explanation
- Prediction confidence
- Top contributing events
- Risk level
- Root cause analysis
- Event-wise recommendations
- Feature importance visualization


---

# Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Dashboard | Streamlit |
| Machine Learning | Scikit-learn |
| Explainability | SHAP |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Model Storage | Joblib |
| Version Control | Git & GitHub |

---

# Installation

Clone the repository

```bash
git clone <repository-link>
```

Move into the project

```bash
cd Intelligent-Log-Analytics-Anomaly-Detection-Platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶Running the Project

Run the Streamlit application

```bash
streamlit run dashboard/Home.py
```

The dashboard opens at

```
http://localhost:8501
```

---

# Dataset

Due to GitHub file size limitations, the dataset is **not included** in this repository.

Download the dataset from:

**https://github.com/logpai/loghub** (please download the first dataset in this repo)

Place the following file inside the `data/` directory:

```
data/Event_occurrence_matrix.csv
```

---

# Performance

Model:

Random Forest Classifier

Evaluation Metrics:

- Accuracy ≈ 99%
- Precision ≈ 99%
- Recall ≈ 99%
- F1 Score ≈ 99%

*(Results may vary depending on the dataset used.)*

---

# Future Scope

- Real-time log streaming
- Cloud deployment
- Multi-dataset support
- LLM-powered natural language explanations
- Deep Learning based anomaly detection
- Integration with Hadoop clusters
- Email/SMS alert system
- Role-based authentication

---

# Team

- Ridhima Pant
- Ashika Adhirai
- Neeraj

---
