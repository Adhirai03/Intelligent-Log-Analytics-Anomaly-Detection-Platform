import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

st.title("🔍 Anomaly Detection")

df = pd.read_csv(
    ROOT_DIR / "data" / "Event_occurrence_matrix.csv"
)

# Load model lazily after a Block ID is selected to avoid crashing the
# page if the model file is missing or corrupted.

features = [f"E{i}" for i in range(1,30)]

st.subheader("Select a Log Record")

# Ensure BlockId options are strings and remove NaNs/duplicates
block_options = (
    df["BlockId"]
    .dropna()
    .astype(str)
    .unique()
)

selected_block = st.selectbox(
    "Choose a Block ID",
    block_options
)

# Compare as strings to match the selectbox options
row = df[df["BlockId"].astype(str) == str(selected_block)]

# Lazy-load model now that a selection exists
model = None
try:
    model = joblib.load(ROOT_DIR / "saved_models" / "random_forest.pkl")
except Exception as e:
    st.warning(f"Model could not be loaded: {e}")
    # Allow the page to continue and show predicted info only if model loads

if not row.empty:

    st.success("Block Found")

    actual_label = row["Label"].iloc[0]

    st.write("Actual Label:", actual_label)


    if model is not None:
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
    else:
        st.info("Model not available — predictions are disabled.")
    # Severity (only shown when model available)
    if model is not None:
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