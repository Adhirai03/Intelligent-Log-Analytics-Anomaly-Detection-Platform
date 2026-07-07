import streamlit as st
import joblib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

st.title("🔍 Anomaly Detection")

# -------------------------------
# Check if data is available
# -------------------------------
if st.session_state.get("uploaded_file") is None:
    st.warning(
        "⚠️ No data found. Please go to the **Home** page and upload a file first."
    )
    st.stop()

# Use uploaded dataset
df = st.session_state["uploaded_file"]

# -------------------------------
# Feature Columns
# -------------------------------
features = [f"E{i}" for i in range(1, 30)]

# Verify required columns exist
missing_cols = [col for col in features if col not in df.columns]

if missing_cols:
    st.error(f"Dataset is missing required columns: {missing_cols}")
    st.stop()

# -------------------------------
# Block Selection
# -------------------------------
st.subheader("Select a Log Record")

block_ids = sorted(df["BlockId"].dropna().astype(str).unique())

if not block_ids:
    st.error("No Block IDs found in the uploaded dataset.")
    st.stop()

search_query = st.text_input(
    "Search Block ID",
    placeholder="Type part of a Block ID"
)

filtered_block_ids = [
    block_id
    for block_id in block_ids
    if search_query.lower() in block_id.lower()
]

if not filtered_block_ids:
    st.warning("No matching Block IDs found.")
    st.stop()

selected_block = st.selectbox(
    "Choose a Block ID",
    filtered_block_ids
)

# -------------------------------
# Selected Row
# -------------------------------
row = df[df["BlockId"].astype(str) == selected_block]

if row.empty:
    st.error("Block ID not found.")
    st.stop()

st.success("✅ Block Found")

# -------------------------------
# Actual Label
# -------------------------------
actual_label = row["Label"].iloc[0]
st.write("### Actual Label")
st.write(actual_label)

# -------------------------------
# Load Model
# -------------------------------
try:
    model = joblib.load(ROOT_DIR / "saved_models" / "random_forest.pkl")
except Exception as e:
    st.error(f"Unable to load model.\n\n{e}")
    st.stop()

# -------------------------------
# Prediction
# -------------------------------
prediction = model.predict(row[features])[0]
probability = model.predict_proba(row[features])[0]

anomaly_confidence = probability[1] * 100

predicted_label = "Anomaly" if prediction == 1 else "Normal"

st.write("### Predicted Label")
st.write(predicted_label)

# -------------------------------
# Confidence
# -------------------------------
st.subheader("Prediction Confidence")

st.progress(float(anomaly_confidence / 100))

st.write(f"Anomaly Probability: **{anomaly_confidence:.2f}%**")

# -------------------------------
# Severity
# -------------------------------
if anomaly_confidence >= 80:
    severity = "🔴 High"
elif anomaly_confidence >= 50:
    severity = "🟡 Medium"
else:
    severity = "🟢 Low"

st.write("### Severity Level")
st.write(severity)

# -------------------------------
# Top Event Occurrences
# -------------------------------
st.subheader("Top Event Occurrences")

event_values = (
    row[features]
    .T
    .rename(columns={row.index[0]: "Count"})
    .sort_values(by="Count", ascending=False)
)

st.dataframe(
    event_values.head(10),
    width="stretch"
)

# -------------------------------
# Complete Event Pattern
# -------------------------------
st.subheader("Complete Event Pattern")

st.dataframe(
    row[features].T,
    width="stretch"
)