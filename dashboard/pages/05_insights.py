import streamlit as st

from explainability.shap_analysis import (
    predict_row,
    prediction_probability,
    generate_explanation,
    feature_importance_plot
)

from insights.recommendations import build_ai_insight

st.title("Actionable Insights")
if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]
    row = st.number_input(
        "Execution Trace",
        0,
        575061,
        15
    )

    prediction = predict_row(row)

    confidence = prediction_probability(row)

    st.metric(
        "Prediction",
        prediction
    )

    st.metric(
        "Confidence",
        f"{confidence}%"
    )

    st.divider()

    st.subheader("Model Explanation")

    st.write(generate_explanation(row))

    fig = feature_importance_plot(row)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    report = build_ai_insight(row)

    st.subheader("Risk Level")

    st.error(report["risk"])

    st.subheader("Detected Events")

    for item in report["events"]:

        with st.expander(item["title"]):

            st.write("Cause")

            st.info(item["cause"])

            st.write("Recommendation")

            st.success(item["recommendation"])
else:
    st.warning("⚠️ No data found. Please go to the **'Home'** page and upload a file first.   ")