from pathlib import Path

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def show_report(
    selected_block=None,
    occurrence_row=None,
    predicted_label=None,
    confidence=None,
    top10=None,
    output_path="Model_Analytics_Report.pdf",
):
    pdf = SimpleDocTemplate(output_path)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("<b>Model Analytics Report</b>", styles["Title"]))

    story.append(Paragraph(f"Block ID : {selected_block}", styles["BodyText"]))

    if occurrence_row is not None and not occurrence_row.empty:
        if "Label" in occurrence_row.columns:
            story.append(
                Paragraph(f"Actual Label : {occurrence_row['Label'].iloc[0]}", styles["BodyText"])
            )

        if "Type" in occurrence_row.columns:
            story.append(
                Paragraph(f"Failure Type : {occurrence_row['Type'].iloc[0]}", styles["BodyText"])
            )

    if predicted_label is not None:
        story.append(Paragraph(f"Predicted Label : {predicted_label}", styles["BodyText"]))

    if confidence is not None:
        story.append(
            Paragraph(f"Prediction Confidence : {float(confidence):.2f}%", styles["BodyText"])
        )

    story.append(Paragraph("<b>Top Important Features</b>", styles["Heading2"]))

    if top10 is not None:
        for _, row in top10.iterrows():
            story.append(
                Paragraph(f"{row['Feature']} : {row['Importance']:.4f}", styles["BodyText"])
            )

    pdf.build(story)
    return Path(output_path).resolve()