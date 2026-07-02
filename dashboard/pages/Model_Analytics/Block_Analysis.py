import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dashboard.pages.Model_Analytics.Report_generator import show_report
from collections import Counter

ROOT_DIR = Path(__file__).resolve().parents[3]


@st.cache_data(show_spinner=False)
def load_trace_data():
    return pd.read_csv(ROOT_DIR / "HDFS_v1" / "data" / "Event_traces.csv")


@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(ROOT_DIR / "saved_models" / "random_forest.pkl")


def show_block_analysis():
    # -------------------------
    # Load Data & Model
    # -------------------------
    df = st.session_state.get("df")

    if df is None or df.empty:
        st.warning("Please upload dataset first in Upload tab")
        st.stop()

    trace_df = load_trace_data()
    model = load_model()

    features = [f"E{i}" for i in range(1, 30)]

    # -------------------------
    # UI
    # -------------------------

    block_ids = sorted(df["BlockId"].dropna().astype(str).unique())

    if not block_ids:
        st.error("No block IDs are available in the uploaded dataset.")
        st.stop()

    search_query = st.text_input(
        "Search Block ID",
        value="",
        placeholder="Type part of a Block ID",
        help="Use this to quickly find a block when the list is large."
    )

    filtered_block_ids = [
        block_id for block_id in block_ids
        if search_query.lower() in block_id.lower()
    ] if search_query else block_ids

    if not filtered_block_ids:
        st.warning("No matching Block IDs found. Try a different search term.")
        st.stop()

    selected_block = st.selectbox(
        "Select Block ID",
        filtered_block_ids,
        index=0,
        key="block_selector"
    )

    occurrence_row = df[df["BlockId"].astype(str) == selected_block]
    trace_row = trace_df[trace_df["BlockId"].astype(str) == selected_block]

    if occurrence_row.empty:
        st.warning("No data found for selected block")
        st.stop()

    # -------------------------
    # Prediction
    # -------------------------
    prediction = model.predict(occurrence_row[features])[0]
    probability = model.predict_proba(occurrence_row[features])[0]
    confidence = probability[prediction] * 100
    predicted_label = "Fail" if prediction == 1 else "Success"

    # -------------------------
    # Feature Importance (GLOBAL)
    # -------------------------
    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    top10 = importance_df.head(10)

    # Save results in session state
    st.session_state.selected_block = selected_block
    st.session_state.occurrence_row = occurrence_row
    st.session_state.predicted_label = predicted_label
    st.session_state.confidence = confidence
    st.session_state.top10 = top10


    st.success("Analysis Completed")

    c1, c2, c3 = st.columns(3)

    c1.metric("Actual Label", occurrence_row["Label"].iloc[0])
    c2.metric("Predicted Label", predicted_label)
    c3.metric("Confidence", f"{confidence:.2f}%")

    st.markdown("---")

    # -------------------------
    # Block Details
    # -------------------------

    st.header("📊 Event Summary")

    if not trace_row.empty:

        events = trace_row["Features"].iloc[0]
        events = events.strip("[]").split(",")

        counter = Counter(events)

        most_event = counter.most_common(1)[0][0]

        latency = trace_row["Latency"].iloc[0]

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Total Events", len(events))
        c2.metric("Unique Events", len(counter))
        c3.metric("Most Frequent", most_event)
        c4.metric("Latency (ms)", latency)
        c5.metric("Failure Type", occurrence_row["Type"].iloc[0])

        st.markdown("---")

        # Event Timeline

        st.subheader("Event Timeline")

        timeline = " ➜ ".join(events[:30])

        st.info(timeline)

        if len(events) > 30:
            st.caption("Showing first 30 events")

        st.markdown("---")

        # Latency Gauge

        st.subheader("⚡ Latency Analysis")

        fig = go.Figure(go.Indicator(

            mode="gauge+number",

            value=float(latency),

            title={"text":"Latency (ms)"},

            gauge={
                "axis":{"range":[0,5000]},
                "bar":{"color":"red"},
                "steps":[
                    {"range":[0,1500],"color":"lightgreen"},
                    {"range":[1500,3000],"color":"yellow"},
                    {"range":[3000,5000],"color":"salmon"}
                ]
            }

        ))

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # Feature Importance (GLOBAL)
    # -------------------------
    st.header("Feature Analysis")

    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    top10 = importance_df.head(10)

    fig = px.bar(top10, x="Feature", y="Importance", text="Importance")
    st.plotly_chart(fig, width="stretch")

    st.dataframe(top10, width="stretch")

    # -------------------------
    # Selected Block Events
    # -------------------------
    st.header("Block Event Analysis")

    selected_events = occurrence_row[features].T
    selected_events.columns = ["Occurrence"]

    selected_events = selected_events[selected_events["Occurrence"] > 0]
    selected_events = selected_events.sort_values(
        by="Occurrence",
        ascending=False
    )

    top_events = selected_events.head(10).reset_index()
    top_events.columns = ["Event", "Occurrence"]

    fig_events = px.line(
        top_events,
        x="Event",
        y="Occurrence",
        markers=True,
        text="Occurrence",
        title="Top 10 Event Occurrences in Selected Block"
    )

    fig_events.update_traces(
        mode="lines+markers+text",
        textposition="top center"
    )

    fig_events.update_layout(
        xaxis_title="Events",
        yaxis_title="Occurrence Count",
        hovermode="x unified"
    )

    st.plotly_chart(fig_events, width="stretch")

    st.dataframe(
        selected_events,
        width="stretch"
    )

    # -------------------------
    # Model Explanation Match
    # -------------------------
    st.header("Model Decision Explanation")

    top_model_features = set(importance_df.head(10)["Feature"])
    block_features = set(selected_events.index)

    matching = list(block_features.intersection(top_model_features))

    if matching:

        st.success("The Random Forest model predicted this block as anomalous because:")

        for event in matching:

            imp = importance_df.loc[
                importance_df["Feature"]==event,
                "Importance"
            ].values[0]

            occ = selected_events.loc[event,"Occurrence"]

            st.write(
                f"✅ **{event}** occurred **{int(occ)}** times and has a feature importance of **{imp:.3f}**."
            )

    else:

        st.warning("No highly important events were detected in this block.")

    st.markdown("---")

    st.header("🔍 Possible Root Cause")

    causes=[]

    if not trace_row.empty:

        latency = trace_row["Latency"].iloc[0]

        if latency>3000:
            causes.append("High latency observed during block execution.")

    if occurrence_row["Type"].iloc[0]!=0:
        causes.append(
            f"Failure Type {occurrence_row['Type'].iloc[0]} indicates abnormal execution."
        )

    if "E3" in counter:
        causes.append("Repeated occurrence of E3 event.")

    if "E26" in counter:
        causes.append("Frequent block replication activity (E26).")

    if causes:

        for cause in causes:
            st.warning(cause)

    else:

        st.success("No major root causes identified.")

    st.markdown("---")

    st.header("💡 Suggested Actions")

    actions=[]

    if not trace_row.empty and latency>3000:
        actions.append("Check DataNode network latency.")

    if occurrence_row["Type"].iloc[0]!=0:
        actions.append("Review HDFS error logs.")

    if "E3" in counter:
        actions.append("Inspect block replication service.")

    if "E26" in counter:
        actions.append("Verify storage node health.")

    if predicted_label=="Fail":
        actions.append("Monitor this block for repeated failures.")

    if actions:

        for action in actions:
            st.info(action)

    else:

        st.success("No corrective actions required.")

    # -------------------------
    # Generate Report Button
    # -------------------------
    if st.button("📄 Generate Model Analytics Report"):
        pdf_path = show_report(
            selected_block=st.session_state.selected_block,
            occurrence_row=st.session_state.occurrence_row,
            predicted_label=st.session_state.predicted_label,
            confidence=st.session_state.confidence,
            top10=st.session_state.top10,
        )
        st.success(f"Report generated successfully: {pdf_path}")
        st.write(f"[Download Report]({pdf_path})")