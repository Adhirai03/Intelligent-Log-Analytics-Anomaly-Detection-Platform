import streamlit as st
from dashboard.pages.Model_Analytics.Data_review import show_review
from dashboard.pages.Model_Analytics.Block_Analysis import show_block_analysis
from dashboard.pages.Model_Analytics.Report_generator import show_report

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

local_css("dashboard/css/model_analysis.css")

st.markdown("""
<div class="model-hero">
<h1> Model Analytics Dashboard</h1>
<p>
Analyze execution traces using the trained Random Forest model,
explore execution patterns, understand predictions,
and generate professional analytics reports.
</p>
</div>
""", unsafe_allow_html=True)

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
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.header("Dataset Review")
            st.success("Dataset loaded successfully. Review the uploaded data before analysing individual execution blocks.")
            show_review()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.")

with tab2:
    if st.session_state.get("uploaded_file") is None:
        st.warning("⚠️ No data found. Please go to the **Home** page and upload a file first.")
    else:
        st.header("Block Analysis")

        st.info(
            "Select an execution block to inspect model predictions, "
            "feature importance, event patterns and AI explanations."
        )

        show_block_analysis()

with tab3:        
    st.header("Report Generator")

    if st.session_state.get("selected_block") is None:
        st.warning(
            "Analyze a block first before generating the report."
        )

    else:
        with st.container(border=True):
            col1, col2 = st.columns([2,1])
            with col1:
                st.write(
                    f"Selected Block : "
                    f"{st.session_state.selected_block}"
                )

                st.write(
                    f"Prediction : "
                    f"{st.session_state.predicted_label}"
                )

                st.write(
                    f"Confidence : "
                    f"{st.session_state.confidence:.2f}%"
                )

            with col2:
                st.metric(
                    "Top Features",
                    len(st.session_state.top10)
                    if st.session_state.top10 is not None
                    else 0
                )
        
        st.markdown("---")

        if st.button(
            "Generate Model Analytics Report",
            use_container_width=True
        ):
            pdf_path = show_report(
                selected_block=st.session_state.selected_block,
                occurrence_row=st.session_state.occurrence_row,
                predicted_label=st.session_state.predicted_label,
                confidence=st.session_state.confidence,
                top10=st.session_state.top10
            )

            st.success(
                "Report generated successfully."
            )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF Report",
                    data=f,
                    file_name=pdf_path.name,
                    mime="application/pdf",
                    use_container_width=True
                )
    