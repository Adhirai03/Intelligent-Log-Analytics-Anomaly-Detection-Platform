import streamlit as st
import pandas as pd
import plotly.express as px

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("dashboard/css/alert.css")

st.markdown("""
<div class="alert-hero">
    <h1>🚨 Alerts & Failures Dashboard</h1>
    <p>Monitor anomalies, investigate failure patterns, and export alert reports.</p>
</div>
""", unsafe_allow_html=True)

if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]

    alerts = df[df["Label"] == "Fail"]
    total = len(df)
    total_alerts = len(alerts)
    rate = round((total_alerts / total) * 100, 2) if total else 0

    c1, c2, c3 = st.columns(3)
    cards = [
        ("Total Alerts", total_alerts, "#EF4444"),
        ("Alert Rate", f"{rate}%", "#F59E0B"),
        ("Healthy Logs", total-total_alerts, "#22C55E")
    ]

    for col, (title, value, color) in zip([c1,c2,c3], cards):
        with col:
            st.markdown(f'''
            <div class="metric-card" style="border-left-color:{color}">
                <div class="metric-title">{title}</div>
                <div class="metric-value" style="color:{color}">{value}</div>
            </div>
            ''', unsafe_allow_html=True)

    with st.container(border=False):
        st.markdown("")
        st.subheader("Failure Type Distribution")

        type_counts = (
            alerts["Type"].value_counts().reset_index()
        )
        type_counts.columns = ["Failure Type", "Count"]

        fig = px.bar(
            type_counts,
            x="Failure Type",
            y="Count",
            text="Count",
            color="Count",
            color_continuous_scale="Reds"
        )
        fig.update_traces(
            textposition="outside"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#172033",
            plot_bgcolor="#172033",
            font_color="white",
            margin=dict(l=20,r=20,t=40,b=20)
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
    with st.container(border=False):
        st.subheader("📥 Export Alert Report")
        st.download_button(
            label="Download Alert Report",
            data=csv,
            file_name="alerts_report.csv",
            mime="text/csv",
        )
else:
    st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.   ")