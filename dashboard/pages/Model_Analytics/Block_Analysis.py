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

    # Load Data & Model
    df = st.session_state.get("uploaded_file")

    if df is None or df.empty:
        st.warning("Please upload dataset first in Upload tab")
        st.stop()

    model = load_model()

    features = [f"E{i}" for i in range(1, 30)]

    block_ids = sorted(df["BlockId"].dropna().astype(str).unique())

    if not block_ids:
        st.error("No block IDs are available in the uploaded dataset.")
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

        occurrence_row = df[df["BlockId"].astype(str) == selected_block]

        if occurrence_row.empty:
            st.warning("No data found for selected block")
            st.stop()

    # Prediction
    prediction = model.predict(occurrence_row[features])[0]
    probability = model.predict_proba(occurrence_row[features])[0]
    confidence = probability[prediction] * 100
    predicted_label = "Fail" if prediction == 1 else "Success"

    # Feature Importance (GLOBAL)
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

    c1,c2,c3 = st.columns(3)

    cards = [
        ("Actual", occurrence_row["Label"].iloc[0],
        "#22C55E" if str(occurrence_row["Label"].iloc[0]).lower()=="success" else "#EF4444"),
        ("Prediction", predicted_label,
        "#EF4444" if predicted_label=="Fail" else "#22C55E"),
        ("Confidence", f"{confidence:.2f}%", "#F59E0B"),
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

    # Feature Importance (GLOBAL)
    st.header("Feature Analysis")

    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    top10 = importance_df.head(10).copy()

    # Round importance to 4 decimal places so graph values are clean
    top10["Importance"] = top10["Importance"].round(4)
    top10["ImportanceRounded"] = top10["Importance"].apply(lambda x: f"{x:.4f}")

    fig = px.bar(
        top10,
        x="Feature",
        y="Importance",
        text="ImportanceRounded",
        color="Importance",
        color_continuous_scale="Blues"
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont_size=12,
        cliponaxis=False
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        margin=dict(l=40, r=20, t=40, b=80),
        yaxis=dict(
            tickformat=".4f",
            dtick=0.05
        )
    )
    fig.update_coloraxes(
        cmin=0,
        cmax=0.17
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display clean table with only Feature and rounded Importance
    display_df = top10[["Feature", "Importance"]].reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("---")


    # Selected Block Events

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
        hovermode="x unified",
        margin=dict(l=40, r=20, t=40, b=80),
    )

    st.plotly_chart(fig_events, width="stretch")

    st.dataframe(
        selected_events,
        width="stretch"
    )

    st.markdown("---")


    # Model Explanation Match

    st.header("Model Decision Explanation")

    top_model_features = set(importance_df.head(10)["Feature"])
    block_features = set(selected_events.index)

    matching = list(block_features.intersection(top_model_features))

    if matching:

        st.success(
            f"The Random Forest model predicted **{predicted_label}** because these events had the highest contribution."
        )
        explanation = []
        for event in matching:

            imp = importance_df.loc[
                importance_df["Feature"]==event,
                "Importance"
            ].values[0]

            occ = int(selected_events.loc[event,"Occurrence"])
            score = imp * occ
            explanation.append(
                {
                    "event":event,
                    "occ":occ,
                    "importance":imp,
                    "score": score,
                }
            )
        explanation=sorted(
            explanation,
            key=lambda x:x["importance"],
            reverse=True
        )

        for i, row in enumerate(explanation[ :5]):
            st.markdown(
                f"""
                <div class="model-card">
                    <div class="model-left">
                        <div class="event-title">
                            {row['event']}      
                        </div>
                        <div class="event-text">
                            Occurred :
                            <b>{row['occ']}</b> times
                        </div>
                        <div class="event-text">
                            Feature Importance :
                            <b>{row['importance']:.3f}</b>
                        </div>
                    </div>
                    <div class="model-right">
                        <div class="importance-label">
                            Importance
                        </div>
                        <div class="importance-value">
                            {row['importance']*100:.1f}%
                        </div>
                        <div class="progress">
                            <div class="progress-fill"
                                style="width:{row['importance']*100}%">
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True,
            )
    else:
        st.warning("No highly important events were detected in this block.")

    st.markdown("---")