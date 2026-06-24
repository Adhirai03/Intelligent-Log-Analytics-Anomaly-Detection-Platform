import streamlit as st
import plotly.express as px
import numpy as np
import joblib
import pandas as pd

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

st.markdown("---")

# Load Random Forest Model
model = joblib.load(
    "saved_models/random_forest.pkl"
)

features = [f"E{i}" for i in range(1,30)]

# Feature Importance
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

st.subheader("Top Important Events")

fig_imp = px.bar(
    importance_df.head(15),
    x="Feature",
    y="Importance",
    title="Top 15 Most Important Events"
)

st.plotly_chart(fig_imp, use_container_width=True)

st.subheader("Feature Importance Table")

st.dataframe(
    importance_df,
    use_container_width=True
)