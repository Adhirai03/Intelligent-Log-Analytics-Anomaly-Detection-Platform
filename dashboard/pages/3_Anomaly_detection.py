import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

st.title("🔍 Anomaly Detection")

df = pd.read_csv(
    ROOT_DIR / "HDFS_v1" / "data" / "Event_occurrence_matrix.csv"
)

model = joblib.load(
    ROOT_DIR / "saved_models" / "random_forest.pkl"
)

features = [f"E{i}" for i in range(1,30)]

st.subheader("Select a Log Record")

selected_block = st.selectbox(
    "Choose a Block ID",
    df["BlockId"].unique()
)

row = df[df["BlockId"] == selected_block]

if not row.empty:

    st.success("Block Found")

    actual_label = row["Label"].iloc[0]

    st.write("Actual Label:", actual_label)

    prediction = model.predict(row[features])[0]

    probability = model.predict_proba(row[features])[0]

    anomaly_confidence = probability[1] * 100

    pred_label = (
        "Anomaly"
        if prediction == 1
        else "Normal"
    )

    st.write("Predicted Label:", pred_label)

    # Confidence
    st.subheader("Prediction Confidence")

    st.progress(anomaly_confidence / 100)

    st.write(
        f"Anomaly Probability: {anomaly_confidence:.2f}%"
    )

    # Severity
    if anomaly_confidence >= 80:
        severity = "🔴 High"
    elif anomaly_confidence >= 50:
        severity = "🟡 Medium"
    else:
        severity = "🟢 Low"

    st.write("Severity Level:", severity)

    # Top Events
    st.subheader("Top Event Occurrences")

    event_values = row[features].T
    event_values.columns = ["Count"]

    event_values = event_values.sort_values(
        by="Count",
        ascending=False
    )

    st.dataframe(
        event_values.head(10),
        use_container_width=True
    )

    # Complete Pattern
    st.subheader("Complete Event Pattern")

    st.dataframe(
        row[features].T,
        use_container_width=True
    )

else:
    st.error("Block ID not found")