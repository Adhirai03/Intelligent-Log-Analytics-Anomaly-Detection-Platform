import streamlit as st
import plotly.express as px
from pathlib import Path

from utils.log_analysis import (
    load_data,
    get_total_logs,
    get_success_fail_counts,
    get_failure_type_distribution,
    get_top_events
)

ROOT_DIR = Path(__file__).resolve().parents[2]

st.title("📊 Log Overview")

# Load Dataset

if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]

    # Total Logs
    total_logs = get_total_logs(df)

    st.metric(
        label="Total Log Traces",
        value=f"{total_logs:,}"
    )

    # Success vs Fail
    st.subheader("Success vs Fail Distribution")

    success_fail = get_success_fail_counts(df)

    fig1 = px.pie(
        values=success_fail.values,
        names=success_fail.index,
        title="Success vs Fail Logs"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Failure Types
    st.subheader("Failure Type Distribution")

    failure_types = get_failure_type_distribution(df)

    fig2 = px.bar(
        x=failure_types.index,
        y=failure_types.values,
        labels={
            "x": "Failure Type",
            "y": "Count"
        },
        title="Failure Type Counts"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Top Events
    st.subheader("Top Event Templates")

    top_events = get_top_events(df)

    fig3 = px.bar(
        x=top_events.index,
        y=top_events.values,
        labels={
            "x": "Event",
            "y": "Occurrences"
        },
        title="Most Frequent Events"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.dataframe(top_events)
else:
    st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.   ")