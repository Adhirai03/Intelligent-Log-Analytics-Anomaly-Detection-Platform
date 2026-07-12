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

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

local_css("dashboard/css/log_overview.css")

def card(title, value, color):
    st.markdown(f"""
    <div class="ov-card" style="border-top:5px solid {color}">
        <div class="ov-title">{title}</div>
        <div class="ov-value" style="color:{color}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="overview-banner">
<h1>Log Overview Dashboard</h1>
<p>Summary of uploaded logs and anomaly distribution</p>
</div>
""", unsafe_allow_html=True)

if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]

    total = get_total_logs(df)
    sf = get_success_fail_counts(df)
    success = int(sf.get("Success",0))
    fail = int(sf.get("Fail",0))
    rate = round(fail/total*100,2) if total else 0

    # Success vs Fail
    sf = get_success_fail_counts(df)
    left,right = st.columns(2)
    with left:
        st.subheader("Success vs Fail Distribution")
        with st.container(border=False):
            fig = px.pie(
                values=sf.values,
                names=sf.index,
                hole=.55,
                color=sf.index,
                color_discrete_sequence=["#22c55e","#ef4444"]
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#162032",
                plot_bgcolor="#162032",
                margin=dict(l=20,r=20,t=40,b=20)
            )
            st.plotly_chart(fig,use_container_width=True)

    with right:
        st.subheader("Failure Type Distribution")
        ft = get_failure_type_distribution(df)
        fig2 = px.bar(
            x=ft.index,
            y=ft.values,
            text=ft.values,
            labels={
                "x": "Failure Type",
                "y": "Frequency"
            },
            color=ft.values,
            color_continuous_scale="Reds"
        )
        # fig2.update_traces(marker_color="#60a5fa")
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#162032",
            plot_bgcolor="#162032"
        )
        st.plotly_chart(fig2,use_container_width=True)

    # Top Events
    with st.container(border=False):
        st.subheader("Top Event Templates")
        te = get_top_events(df)

        fig3 = px.bar(
            x=te.values,
            y=te.index,
            labels={
                "x": "Occurrences",
                "y": "Event"
            },
            title="Most Frequent Events",
            orientation="h",
            color=te.values,
            color_continuous_scale="Blues"
        )
        fig3.update_yaxes(autorange="reversed")
        fig3.update_coloraxes(
            cmin=0,
            cmax=5200
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.subheader("Event Frequency Table")
    st.dataframe(te.reset_index().rename(columns={"index":"Event",0:"Occurrences"}),use_container_width=True,height=350)
else:
    st.warning("⚠️ No data found. Please go to the **'Home'** page and upload a file first.   ")