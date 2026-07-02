import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚨 Alerts & Failures")
if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]

    alerts = df[df["Label"] == "Fail"]

    st.metric(
        "Total Anomalies",
        len(alerts)
    )

    st.subheader("Failure Type Distribution")

    type_counts = (
        alerts["Type"]
        .value_counts()
        .reset_index()
    )

    fig = px.bar(
        type_counts,
        x="Type",
        y="count",
        title="Failure Types"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Recent Anomalous Blocks")

    st.dataframe(
        alerts[
            ["BlockId", "Type", "Label"]
        ].head(100),
        use_container_width=True
    )

    csv = alerts.to_csv(index=False)

    st.download_button(
        label="Download Alert Report",
        data=csv,
        file_name="alerts.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.   ")