import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

st.title("🤖 Model Analytics")

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", "99.99%")
col2.metric("Precision", "99.85%")
col3.metric("Recall", "99.91%")
col4.metric("F1 Score", "99.88%")

st.markdown("---")

# Confusion Matrix
st.subheader("Confusion Matrix")

cm = np.array([
    [111640, 5],
    [3, 3365]
])

fig_cm = px.imshow(
    cm,
    text_auto=True,
    labels=dict(
        x="Predicted Label",
        y="Actual Label"
    ),
    x=["Normal", "Anomaly"],
    y=["Normal", "Anomaly"]
)

st.plotly_chart(fig_cm, use_container_width=True)

st.info(
    """
    True Negatives : 111640
    
    False Positives : 5
    
    False Negatives : 3
    
    True Positives : 3365
    """
)

st.markdown("---")

# Load Model
model = joblib.load(
    ROOT_DIR /"saved_models" / "random_forest.pkl"
)

features = [f"E{i}" for i in range(1,30)]

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

# Top Important Events
st.subheader("Top Important Events")

fig_imp = px.bar(
    importance_df.head(15),
    x="Feature",
    y="Importance",
    title="Top 15 Most Important Events"
)

st.plotly_chart(fig_imp, use_container_width=True)

# Top 5 Event Cards
st.subheader("Most Influential Events")

top5 = importance_df.head(5)

cols = st.columns(5)

for idx, (_, row) in enumerate(top5.iterrows()):
    cols[idx].metric(
        row["Feature"],
        f"{row['Importance']:.4f}"
    )

st.markdown("---")

# Feature Table
st.subheader("Feature Importance Table")

st.dataframe(
    importance_df,
    use_container_width=True
)

st.markdown("---")

# Model Summary
st.subheader("Model Insights")

st.success(
    f"""
    Random Forest identified {importance_df.iloc[0]['Feature']}
    as the most influential event contributing to anomaly detection.

    The model demonstrates excellent performance with high
    precision and recall, making it suitable for detecting
    anomalous HDFS log patterns.
    """
)