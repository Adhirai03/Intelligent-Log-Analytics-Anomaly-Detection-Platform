import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path
from dashboard.pages.Model_Analytics.Report_generator import show_report

ROOT_DIR = Path(__file__).resolve().parents[3]

@st.cache_resource(show_spinner=False)
def load_model():
    return joblib.load(ROOT_DIR / "saved_models" / "random_forest.pkl")


def show_block_analysis():
    # -------------------------
    # Load Data & Model
    # -------------------------
    df = st.session_state.get("uploaded_file")

    if df is None or df.empty:
        st.warning("Please upload dataset first in Upload tab")
        st.stop()

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

    st.markdown("---")

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

    st.markdown("---")

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