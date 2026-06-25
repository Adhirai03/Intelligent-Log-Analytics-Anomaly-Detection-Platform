import streamlit as st
import pandas as pd
import joblib

st.title("🔍 Log Investigation")

df = pd.read_csv("data/Event_occurrence_matrix.csv")

model = joblib.load(
    "saved_models/random_forest.pkl"
)

features = [f"E{i}" for i in range(1,30)]

block_id = st.text_input(
    "Enter Block ID",
    placeholder="blk_-1608999687919862906"
)

if block_id:

    row = df[df["BlockId"] == block_id]

    if not row.empty:

        st.success("Block Found")

        st.write("Actual Label:", row["Label"].iloc[0])

        prediction = model.predict(
            row[features]
        )[0]

        pred_label = (
            "Anomaly"
            if prediction == 1
            else "Normal"
        )

        st.write("Predicted Label:", pred_label)

        st.subheader("Event Pattern")

        st.dataframe(
            row[features].T,
            use_container_width=True
        )

    else:
        st.error("Block ID not found")