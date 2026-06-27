import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Intelligent Log Analytics",
    layout="wide"
)

st.title("🔍 Intelligent Log Analytics & Anomaly Detection Platform")
st.markdown("##### AI-powered execution tracing, early incident detection, and actionable root-cause insights.")

st.markdown("### 📥 Ingest Log Sheet")
uploaded_file = st.file_uploader(
    "Drag and drop your raw HDFS execution logs in .csv or .xlsx format.", 
    type=["csv", "xlsx"],
    help="Accepts structured execution sequences mapped by unique BlockId tokens." 
)

if uploaded_file is not None:
    try:
        # Load file locally into memory to display immediate preview structures
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"Successfully loaded '{uploaded_file.name}' locally ({len(df)} records discovered).") 
        df.index = df.index + 1
        st.session_state["uploaded_file"] = df
        Total_logs = len(df)
        Anomalies = len(df[df["Label"] == "Fail"])
        Normal = len(df[df["Label"] == "Success"])
        Anomaly_rate = round((Anomalies / Total_logs) * 100, 2)

        st.markdown("")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Logs", f"{Total_logs:,}")
        col2.metric("Normal Logs", f"{Normal:,}")
        col3.metric("Anomalies", f"{Anomalies:,}")
        col4.metric("Anomaly Rate", f"{Anomaly_rate}%")

        # Expandable layout to preview raw text configurations before triggering AI pipeline
        with st.expander("👀 View Raw Ingested Log Preview (First 10 Rows)"):
            st.dataframe(df.head(10), width="stretch")

    except Exception as e:
        st.error(f"An unexpected data format error occurred during sheet parsing: {e}") 

else:
    # Baseline visual state layout when no log sheet has been supplied yet [cite: 124]
    st.info("ℹ️ Awaiting HDFS execution logs. Please drag and drop a log tracing file above to run diagnostic analytics.")



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