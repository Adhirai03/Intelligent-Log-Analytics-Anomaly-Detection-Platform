import streamlit as st
import joblib
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

local_css("dashboard/css/anomaly_detection.css")

st.markdown("""
<div class="anomaly-hero">
    <h1>Anomaly Detection</h1>
    <p>
        Detect anomalous HDFS execution traces using the trained
        Random Forest model and visualize execution behaviour.
    </p>
</div>
""", unsafe_allow_html=True)

if st.session_state.get("uploaded_file") is None:
    st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.")
    st.stop()

df = st.session_state["uploaded_file"]

features = [f"E{i}" for i in range(1, 30)]

# Verify required columns exist
missing_cols = [col for col in features if col not in df.columns]

if missing_cols:
    st.error(f"Dataset is missing required columns: {missing_cols}")
    st.stop()

# Block Selection
st.subheader("Select a Log Record")
block_ids = sorted(df["BlockId"].dropna().astype(str).unique())
if not block_ids:
    st.error("No Block IDs found in the uploaded dataset.")
    st.stop()

left,right = st.columns([2,1])

with left:
    search_query = st.text_input(
        "Search Block ID",
        placeholder="Enter part of Block ID..."
    )

filtered_block_ids = [
    block_id
    for block_id in block_ids
    if search_query.lower() in block_id.lower()
]

if not filtered_block_ids:
    st.warning("No matching Block IDs found.")
    st.stop()

with right:
    selected_block = st.selectbox(
        "Choose Block",
        filtered_block_ids
    )

# Selected Row
row = df[df["BlockId"].astype(str) == selected_block]

if row.empty:
    st.error("Selected block ID not found.")
    st.stop()

st.success("✅ Block Found")
st.markdown("")

# Load Model
try:
    model = joblib.load(ROOT_DIR / "saved_models" / "random_forest.pkl")
except Exception as e:
    st.error(f"Unable to load model.\n\n{e}")
    st.stop()

# Prediction
actual_label = row["Label"].iloc[0]
prediction = model.predict(row[features])[0]
probability = model.predict_proba(row[features])[0]
anomaly_confidence = probability[1] * 100
predicted_label = "Anomaly" if prediction == 1 else "Normal"

c1,c2,c3 = st.columns(3)

cards = [
    ("Actual", actual_label,
     "#22C55E" if str(actual_label).lower()=="success" else "#EF4444"),
    ("Prediction", predicted_label,
     "#EF4444" if predicted_label=="Anomaly" else "#22C55E"),
    ("Confidence", f"{anomaly_confidence:.2f}%", "#F59E0B"),
]

for col,(title,value,color) in zip([c1,c2,c3],cards):
    with col:
        st.markdown(f'''
<div class="metric-card" style="border-left-color:{color}">
<div class="metric-title">{title}</div>
<div class="metric-value" style="color:{color}">{value}</div>
</div>
''', unsafe_allow_html=True)

st.markdown("")

# Confidence
left, right = st.columns([3,1])

with left:
    st.subheader("Prediction Confidence")
    st.progress(float(anomaly_confidence/100))
    st.caption(f"Anomaly Probability : {anomaly_confidence:.2f}%")

with right:
    if anomaly_confidence >= 80:
        severity = "🔴 High"
        sev_color = "#EF4444"
    elif anomaly_confidence >= 50:
        severity = "🟡 Medium"
        sev_color = "#F59E0B"
    else:
        severity = "🟢 Low"
        sev_color = "#22C55E"

    st.markdown(f'''
    <div class="metric-card severity" style="border-left-color:{sev_color}">
        <div class="metric-title sev_title">Severity</div>
        <div class="metric-value sev_value" style="color:{sev_color}">
            {severity}
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# Top Event Occurrences
st.subheader("Top Event Occurrences")

event_values = (
    row[features]
    .T
    .rename(columns={row.index[0]: "Count"})
    .sort_values(by="Count", ascending=False)
    .reset_index()
)
event_values.columns=["Event", "Count"]
st.dataframe(
    event_values.head(10),
    width="stretch",
    hide_index=True
)

# Complete Event Pattern
st.subheader("Complete Event Pattern")

event_pattern = (
    row[features]
    .T
    .reset_index()
)

event_pattern.columns = ["Event", "Occurrence"]

st.dataframe(
    event_pattern,
    use_container_width=True,
    hide_index=True
)