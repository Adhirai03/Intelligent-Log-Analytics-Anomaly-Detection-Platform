import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Intelligent Log Analytics",
    layout="wide"
)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("dashboard/style.css")

st.markdown("""
<div class="hero">
    <div>
        <h1> Intelligent Log Analytics Platform</h1>
        <p>
            AI-powered execution tracing • Real-time anomaly detection •
            Root Cause Analysis • Predictive Monitoring
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize the global session state key if it doesn't exist yet
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "file_name" not in st.session_state:
    st.session_state["file_name"] = None

st.markdown("### 📥 Ingest Log Sheet")

# State 1: A file has already been loaded into global memory
if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]
    file_name = st.session_state["file_name"]
    st.success(f"**Active Session Log Loaded '{file_name}':** Metrics and previews are preserved across pages ({len(df)} records active).")
    
    if st.button("Clear Cache & Upload New Log"):
        st.session_state["uploaded_file"] = None
        st.rerun()

# State 2: No file is active in memory;
else:
    uploaded_file = st.file_uploader(
        "Drag and drop your raw HDFS execution logs in .csv or .xlsx format.", 
        type=["csv", "xlsx"],
        help="Accepts structured execution sequences mapped by unique BlockId tokens." 
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            df.index = df.index + 1
            st.session_state["uploaded_file"] = df
            st.session_state["file_name"] = uploaded_file.name
            st.toast(f"Successfully loaded {uploaded_file.name}!", icon="🚀")
            st.rerun()

        except Exception as e:
            st.error(f"An unexpected data format error occurred during sheet parsing: {e}")

# Render metrics and previews if df exists in local memory
if st.session_state["uploaded_file"] is not None:
    df = st.session_state["uploaded_file"]
    Total_logs = len(df)
    Anomalies = len(df[df["Label"] == "Fail"]) if "Label" in df.columns else 0
    Normal = len(df[df["Label"] == "Success"]) if "Label" in df.columns else 0
    Anomaly_rate = round((Anomalies / Total_logs) * 100, 2) if Total_logs > 0 else 0

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)
    cards=[
        ("Total Logs",Total_logs,"#3b82f6","#ffffff"),
        ("Normal Logs",Normal,"#22c55e","#ffffff"),
        ("Anomalies",Anomalies,"#f59e0b","#f59e0b"),
        ("Rate",f"{Anomaly_rate}%","#ef4444","#ef4444")
    ]

    for col,(t,v,b,c) in zip([c1,c2,c3,c4],cards):  
        with col:
            st.markdown(f'''
            <div class="metric-card" style="border-left-color:{b}">
            <div class="metric-title">{t}</div>
            <div class="metric-value" style="color:{c}">{v}</div>
            </div>
            ''',unsafe_allow_html=True)
    st.markdown("")

    # Expandable layout to preview raw text configurations
    with st.expander("View Raw Ingested Log Preview (First 10 Rows)"):
        st.dataframe(df.head(10), use_container_width=True)

    st.markdown("")

    st.subheader("Dataset Information")

    st.markdown("""
    <div style="display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 250px; background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0 0 8px 0; color: #38bdf8; font-size: 1.2rem;">Block & Block ID</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; line-height: 1.4;">Large files are split into blocks. A <code>Block ID</code> tracks a single block's full lifecycle across multiple nodes.</p>
        </div>
        <div style="flex: 1; min-width: 250px; background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #10b981; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0 0 8px 0; color: #34d399; font-size: 1.2rem;">Event</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; line-height: 1.4;">A distinct log action (e.g., <i>"Receiving block"</i>) parsed into a unique template ID (e.g., E1, E2).</p>
        </div>
        <div style="flex: 1; min-width: 250px; background-color: #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0 0 8px 0; color: #fbbf24; font-size: 1.2rem;">Event Trace</h4>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; line-height: 1.4;">The timeline of events for a Block ID, analyzed to flag operations as <b>Normal</b> or <b>Anomaly</b>.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View Event Dictionary  (Log Templates)"):
        st.markdown("This table shows the exact log message template corresponding to each **Event ID** in our dataset.")
        try:
            templates_df = pd.read_csv("data/HDFS.log_templates.csv")
            st.dataframe(templates_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.warning(f"Could not load event templates: {e}")


else:
    st.info(" Awaiting HDFS execution logs. Please drag and drop a log tracing file above to run diagnostic analytics.")

st.sidebar.title("Project Information")
st.sidebar.info("""
Intelligent Log Analytics &
Anomaly Detection Platform

Dataset:
HDFS Event Occurrence Matrix

Model:
Random Forest

Logs:
575,061

Unique Patterns:
589
""")