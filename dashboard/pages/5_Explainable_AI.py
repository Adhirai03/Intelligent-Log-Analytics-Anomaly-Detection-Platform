import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import shap
import numpy as np
import matplotlib.pyplot as plt


st.title("🧠 Explainable AI")

model = joblib.load(
    "saved_models/random_forest.pkl"
)

df = pd.read_csv("data/Event_occurrence_matrix.csv")

features = [f"E{i}" for i in range(1,30)]

X = df[features]


# Random Forest Feature Importance

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

st.subheader("Most Influential Events")

st.dataframe(
    importance_df,
    use_container_width=True
)

fig = px.bar(
    importance_df.head(10),
    x="Feature",
    y="Importance",
    title="Top 10 Important Events"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")


sample_X = X.sample(
    1000,
    random_state=42
)

with st.spinner("Calculating SHAP values..."):

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(sample_X)

    # Your SHAP output shape:
    # (1000, 29, 2)

    anomaly_shap = shap_values[:, :, 1]


st.subheader("SHAP Summary Plot")

fig_shap, ax = plt.subplots(figsize=(10, 6))

shap.summary_plot(
    anomaly_shap,
    sample_X,
    show=False
)

st.pyplot(fig_shap)


mean_shap = np.abs(
    anomaly_shap
).mean(axis=0)

shap_df = pd.DataFrame({
    "Feature": features,
    "SHAP Importance": mean_shap
})

shap_df = shap_df.sort_values(
    by="SHAP Importance",
    ascending=False
)

st.subheader("Top SHAP Features")

st.dataframe(
    shap_df,
    use_container_width=True
)


fig_shap_bar = px.bar(
    shap_df.head(10),
    x="Feature",
    y="SHAP Importance",
    title="Top 10 SHAP Features"
)

st.plotly_chart(
    fig_shap_bar,
    use_container_width=True
)

st.markdown("---")

"""
Random Forest Feature Importance shows which events are globally important.

SHAP explains how each event contributes to anomaly predictions,
making the model more transparent and interpretable.
"""