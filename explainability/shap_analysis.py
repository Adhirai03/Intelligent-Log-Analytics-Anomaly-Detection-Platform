import joblib
import shap
import pandas as pd
import plotly.express as px
from utils.preprocessing import load_data

# Load model
model = joblib.load("saved_models/random_forest.pkl")

# Load dataset
X, y, df = load_data("data/Event_occurrence_matrix.csv")

# Create SHAP explainer
explainer = shap.TreeExplainer(model)

# Internal helper
def _get_single_row_shap(row):
    values = explainer.shap_values(row)

    # SHAP >= 0.45 returns (samples, features, classes)
    if isinstance(values, list):
        return values[1][0]

    # values.shape = (1, 29, 2)
    return values[0, :, 1]

# Top Features
def get_top_features(row_index=0, top_n=5):
    row = X.iloc[[row_index]]
    values = _get_single_row_shap(row)

    importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": abs(values)
    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    return importance.head(top_n)

# Plot
def feature_importance_plot(row_index=0):
    top = get_top_features(row_index)

    fig = px.bar(
        top,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top Events Influencing Prediction"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=420
    )

    return fig

# Explanation
def generate_explanation(row_index=0):
    top = get_top_features(row_index)

    f1 = top.iloc[0]["Feature"]
    f2 = top.iloc[1]["Feature"]
    f3 = top.iloc[2]["Feature"]

    return f"""
The Random Forest model classified this execution trace as anomalous because
the events {f1}, {f2}, and {f3} contributed the most towards the prediction.

These event patterns differ from normal HDFS execution traces observed during
training, making this execution appear suspicious.
""".strip()

# Prediction
def predict_row(row_index=0):
    row = X.iloc[[row_index]]
    pred = model.predict(row)[0]
    return "Anomaly" if pred else "Normal"

# Confidence
def prediction_probability(row_index=0):
    row = X.iloc[[row_index]]
    prob = model.predict_proba(row)[0]
    return round(max(prob) * 100, 2)

# Raw SHAP values
def get_shap_values(row_index=0):
    row = X.iloc[[row_index]]
    return _get_single_row_shap(row)