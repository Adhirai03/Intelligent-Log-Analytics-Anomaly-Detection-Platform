import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Intelligent Log Analytics",
    layout="wide"
)

st.title("🚀 Intelligent Log Analytics & Anomaly Detection Platform")

df = pd.read_csv(
    "C:/Users/Ashika.Adhirai/Downloads/Intelligent Log Analytics & Anomaly Detection Platform/HDFS_v1/data/Event_occurrence_matrix.csv"
)

total_logs = len(df)
anomalies = len(df[df["Label"] == "Fail"])
normal = len(df[df["Label"] == "Success"])

anomaly_rate = round((anomalies / total_logs) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", f"{total_logs:,}")
col2.metric("Normal Logs", f"{normal:,}")
col3.metric("Anomalies", f"{anomalies:,}")
col4.metric("Anomaly Rate", f"{anomaly_rate}%")

st.markdown("---")

st.subheader("Dataset Overview")

st.write(df.head())

st.sidebar.title("Project Information")

st.sidebar.info("""
Intelligent Log Analytics &
Anomaly Detection Platform

Dataset:
HDFS Event Occurrence Matrix

Model:
Random Forest

Logs:
575,061

Unique Patterns:
589
""")