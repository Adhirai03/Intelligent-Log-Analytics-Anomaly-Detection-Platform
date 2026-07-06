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

st.markdown('<link rel="stylesheet" href="dashboard/css/log_overview.css">', unsafe_allow_html=True)

def card(title, value, color):
    st.markdown(f"""
    <div class="ov-card" style="border-top:4px solid {color}">
        <div class="ov-title">{title}</div>
        <div class="ov-value" style="color:{color}">{value}</div>
    </div>
    """, unsafe_allow_html=True)


ROOT_DIR = Path(__file__).resolve().parents[2]

st.markdown("""
<div class="overview-banner">
<h1>📊 Log Overview Dashboard</h1>
<p>Summary of uploaded logs and anomaly distribution</p>
</div>
""", unsafe_allow_html=True)
# Load Dataset

if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]

    # Total Logs
    total = get_total_logs(df)
    sf = get_success_fail_counts(df)
    success = int(sf.get("Success",0))
    fail = int(sf.get("Fail",0))
    rate = round(fail/total*100,2) if total else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1: card("📋 Total Logs", total, "#60a5fa")
    with c2: card("✅ Success", success, "#22c55e")
    with c3: card("🚨 Failed", fail, "#ef4444")
    with c4: card("⚠ Failure %", f"{rate}%", "#f59e0b")
    
    # Success vs Fail
    st.subheader("Success vs Fail Distribution")

    sf = get_success_fail_counts(df)

    left,right = st.columns(2)

    with left:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = px.pie(values=sf.values,names=sf.index,hole=.55,
                    color=sf.index,
                    color_discrete_sequence=["#22c55e","#ef4444"])
        fig.update_layout(template="plotly_dark",paper_bgcolor="#162032",plot_bgcolor="#162032",
                        margin=dict(l=20,r=20,t=40,b=20),title="Success vs Failure")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        ft = get_failure_type_distribution(df)
        fig2 = px.bar(x=ft.index,y=ft.values,text=ft.values)
        fig2.update_traces(marker_color="#60a5fa")
        fig2.update_layout(template="plotly_dark",paper_bgcolor="#162032",plot_bgcolor="#162032",
                        title="Failure Type Distribution")
        st.plotly_chart(fig2,use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


    # Top Events
    st.subheader("Top Event Templates")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    te = get_top_events(df)

    fig3 = px.bar(
        x=te.values,
        y=te.index,
        labels={
            "x": "Occurrences",
            "y": "Event"
        },
        title="Most Frequent Events",
        orientation="h"
    )
    fig3.update_yaxes(autorange="reversed")

    st.plotly_chart(
        fig3,
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Event Frequency Table")
    st.dataframe(te.reset_index().rename(columns={"index":"Event",0:"Occurrences"}),
                use_container_width=True,height=350)
else:
    st.warning("⚠️ No data found. Please go to the **'Home'** page and upload a file first.   ")