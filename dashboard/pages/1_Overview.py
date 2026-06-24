import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Overview")

df = pd.read_csv(
    r"C:/Users/Ashika.Adhirai/Downloads/Intelligent Log Analytics & Anomaly Detection Platform/HDFS_v1/data/Event_occurrence_matrix.csv"
)

features = [f"E{i}" for i in range(1,30)]

# Event Frequency
event_counts = df[features].sum()

fig1 = px.bar(
    x=event_counts.index,
    y=event_counts.values,
    title="Event Frequency"
)

st.plotly_chart(fig1, use_container_width=True)

# Top 10 Events
top_events = event_counts.sort_values(
    ascending=False
).head(10)

fig2 = px.bar(
    x=top_events.index,
    y=top_events.values,
    title="Top 10 Most Frequent Events"
)

st.plotly_chart(fig2, use_container_width=True)

# Success vs Fail
label_counts = df["Label"].value_counts()

fig3 = px.pie(
    values=label_counts.values,
    names=label_counts.index,
    title="Success vs Fail Distribution"
)

st.plotly_chart(fig3, use_container_width=True)