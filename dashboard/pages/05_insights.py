import streamlit as st
from explainability.shap_analysis import (
    predict_row,
    prediction_probability,
    generate_explanation,
    feature_importance_plot
)
from insights.recommendations import build_ai_insight

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("dashboard/css/insight.css")

st.markdown("""
<div class="insight-hero">
    <h1> AI Actionable Insights</h1>
    <p>Explainable AI • Root Cause Analysis • Smart Recommendations</p>
</div>
""", unsafe_allow_html=True)

if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]
    st.subheader("Select Execution Trace")
    row = st.number_input(
        "Execution Trace",
        min_value=0,
        max_value=max(len(df) - 1, 0),
        value=min(15, max(len(df) - 1, 0)),
        step=1,
    )

    prediction = predict_row(row)
    confidence = prediction_probability(row)

    col1, col2, col3 = st.columns(3)
    cards = [
        ("Trace ID", row, "#3B82F6"),
        ("Prediction", prediction,
        "#0BF52A" if str(prediction).lower() == "normal" else "#EF4444"),
        ("Confidence", f"{confidence:.2f}%", "#3FDC5F" if str(prediction).lower() == "normal" else "#F5740B"),
    ]

    for col, (title, value, color) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:{color}">
                <div class="metric-title">{title}</div>
                <div class="metric-value" style="color:{color}">
                    {value}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Model Explanation")
    st.write(generate_explanation(row))

    fig = feature_importance_plot(row)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#172033",
        plot_bgcolor="#172033",
        font_color="white",
        margin=dict(l=20, r=20, t=50, b=20),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    report = build_ai_insight(row)

    st.subheader("Risk Level")
    risk = str(report["risk"]).lower()
    with st.container(border=False):
        if "critical" in risk:
            st.markdown(f"""
            <div class="risk-critical">
                <p>{report["risk"]}</p>
            </div>
            """, unsafe_allow_html=True)

        elif "high" in risk:
            st.markdown(f"""
            <div class="risk-high">
                <p>{report["risk"]}</p>
            </div>
            """, unsafe_allow_html=True)

        elif "medium" in risk:
            st.markdown(f"""
            <div class="risk-medium">
                <p>{report["risk"]}</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class="risk-low">
                <p>{report["risk"]}</p>
            </div>
            """, unsafe_allow_html=True) 

    st.divider()

    st.subheader("Detected Events")
    for i, event in enumerate(report["events"], start=1):
        with st.expander(
            f"Event {i} : {event['title']}",
            expanded=False
        ):
            left, right = st.columns(2)
            with left:
                with st.container(border=False, ):
                    st.markdown("### Root Cause")
                    st.info(event["cause"])

            with right: 
                with st.container(border=False):
                    st.markdown("### Recommendation")
                    st.success(event["recommendation"])

else:
    st.warning("⚠️ No data found. Please go to the **'Home'** page and upload a file first.   ")