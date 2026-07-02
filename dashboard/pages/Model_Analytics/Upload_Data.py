import streamlit as st
import pandas as pd
import plotly.express as px

def show_upload():
    st.write("Upload the HDFS Event Occurrence Matrix dataset to begin the analysis.")

    uploaded_file = st.file_uploader(
        "Upload Event_occurrence_matrix.csv",
        type=["csv"]
    )

    if uploaded_file is not None:
        # Load data and save it globally across tabs
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df
        st.success("Dataset uploaded successfully! Go to the 'Block Analysis' tab to explore.")

        st.markdown("---")

        # ---------------------------------------------------
        # Dataset Summary
        # ---------------------------------------------------
        st.header("📊 Dataset Summary")

        total_blocks = len(df)
        success_blocks = len(df[df["Label"] == "Success"])
        failed_blocks = len(df[df["Label"] == "Fail"])
        failure_percentage = (failed_blocks / total_blocks) * 100 if total_blocks > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Blocks", total_blocks)
        col2.metric("Success Blocks", success_blocks)
        col3.metric("Failed Blocks", failed_blocks)
        col4.metric("Failure %", f"{failure_percentage:.2f}%")

        st.markdown("---")

        # ---------------------------------------------------
        # Success vs Failure Graph
        # ---------------------------------------------------

        st.header("🔥 Event Occurrence Heatmap")

        features = [f"E{i}" for i in range(1, 30)]

        failure_df = df[df["Label"] == "Fail"]

        heatmap_data = (
            failure_df.groupby("Type")[features]
            .sum()
        )

        fig = px.imshow(
            heatmap_data,
            labels=dict(
                x="Events",
                y="Failure Type",
                color="Occurrences"
            ),
            x=features,
            y=heatmap_data.index.astype(str),
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Reds",
            title="Failure Type vs Event Occurrence"
        )

        st.plotly_chart(fig, width="stretch")

        # ---------------------------------------------------
        # Failure Type Analysis
        # ---------------------------------------------------
        st.header("Failure Type Analysis")
        if "Type" in df.columns:
            failure_df = df[df["Label"] == "Fail"]
            failure_count = failure_df["Type"].value_counts().reset_index()
            failure_count.columns = ["Failure Type", "Count"]

            fig_failure = px.bar(failure_count, x="Failure Type", y="Count", text="Count", title="Failure Type Distribution")
            st.plotly_chart(fig_failure, width="stretch")
            st.dataframe(failure_count, width="stretch")
        else:
            st.warning("No 'Type' column found in dataset.")

        st.markdown("---")

        # ---------------------------------------------------
        # Dataset Preview
        # ---------------------------------------------------
        st.header("📋 Dataset Preview")
        st.dataframe(df.head(20), width="stretch")
    else:
        st.info("Please upload Event_occurrence_matrix.csv to continue.")