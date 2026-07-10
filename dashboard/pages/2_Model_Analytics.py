import streamlit as st
from dashboard.pages.Model_Analytics.Data_review import show_review
from dashboard.pages.Model_Analytics.Block_Analysis import show_block_analysis
from dashboard.pages.Model_Analytics.Report_generator import show_report

st.header("🎯 Model Analytics")

if "selected_block" not in st.session_state:
    st.session_state.selected_block = None
if "occurrence_row" not in st.session_state:
    st.session_state.occurrence_row = None
if "predicted_label" not in st.session_state:
    st.session_state.predicted_label = None
if "confidence" not in st.session_state:
    st.session_state.confidence = None
if "top10" not in st.session_state:
    st.session_state.top10 = None

# Initialize isolated Tab views
tab1, tab2, tab3 = st.tabs(["🔍 Data Review", "📊 Block Analysis", "📄 Report"])

with tab1:
        if st.session_state.get("uploaded_file") is not None:
            df = st.session_state["uploaded_file"]
            st.success("Dataset uploaded successfully! Go to the 'Block Analysis' tab to explore.")

            show_review()
        else:
            st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.")

with tab2:
    if st.session_state.get("uploaded_file") is None:
        st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.")
    else:
        show_block_analysis()

with tab3:
    if st.session_state.get("selected_block") is None:
        st.warning("⚠️Please select and analyze a block first.")
    else:
        st.subheader("📄 Generate Report")
        if st.button("Generate Model Analytics Report"):
            pdf_path = show_report(
                selected_block=st.session_state.selected_block,
                occurrence_row=st.session_state.occurrence_row,
                predicted_label=st.session_state.predicted_label,
                confidence=st.session_state.confidence,
                top10=st.session_state.top10,
            )
            st.success("Report generated successfully!")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Report",
                    data=f,
                    file_name=pdf_path.name,
                    mime="application/pdf"
                )
