import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Intelligent Log Analytics",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS file
local_css("dashboard/style.css")

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

        # Create your 4 structural columns
        col1, col2, col3, col4 = st.columns(4)


        card_style = """
            background-color: #1A1F2C; 
            border: 1px solid #2E374A; 
            border-radius: 8px; 
            padding: 20px; 
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
            text-align: center;
        """

        # Column 1: Total Logs
        with col1:
            st.markdown(
                f"""
                <div style="{card_style}">
                    <p style="color: #94A3B8; font-size: 1rem; text-transform: uppercase; margin: 0; letter-spacing: 0.5px;">📋 Total Logs</p>
                    <p style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 10px 0 0 0;">{Total_logs:,}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Column 2: Normal Logs
        with col2:
            st.markdown(
                f"""
                <div style="{card_style}">
                    <p style="color: #94A3B8; font-size: 1rem; text-transform: uppercase; margin: 0; letter-spacing: 0.5px;">✅ Normal Logs</p>
                    <p style="color: #34D399; font-size: 2rem; font-weight: 700; margin: 10px 0 0 0;">{Normal:,}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Column 3: Anomalies
        with col3:
            alert_card_style = card_style + "background-color: #251E2A; border-color: #531f1f;"
            st.markdown(
                f"""
                <div style="{alert_card_style}">
                    <p style="color: #FCA5A5; font-size: 1rem; text-transform: uppercase; margin: 0; letter-spacing: 0.5px;">🚨 Anomalies</p>
                    <p style="color: #F87171; font-size: 2rem; font-weight: 700; margin: 10px 0 0 0;">{Anomalies:,}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Column 4: Anomaly Rate (With a vivid corporate alert background accent)
        with col4:
            alert_card_style = card_style + "background-color: #251E2A; border-color: #EF3333;"
            st.markdown(
                f"""
                <div style="{alert_card_style}">
                    <p style="color: #FCA5A5; font-size: 1rem; text-transform: uppercase; margin: 0; letter-spacing: 0.5px;">⚠️ Anomaly Rate</p>
                    <p style="color: #EF4444; font-size: 2rem; font-weight: 700; margin: 10px 0 0 0;">{Anomaly_rate}%</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        st.markdown("")

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