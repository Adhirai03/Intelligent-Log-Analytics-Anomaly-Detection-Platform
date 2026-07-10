from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def show_report(
    selected_block=None,
    occurrence_row=None,
    predicted_label=None,
    confidence=None,
    top10=None,
    output_path="Model_Analytics_Report.pdf",
):
    pdf = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18
    )
    story = []
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor("#2C3E50"),
        spaceAfter=30,
        alignment=1 # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#2980B9"),
        spaceAfter=12,
        spaceBefore=24
    )

    # Title
    story.append(Paragraph("<b>Model Analytics Report</b>", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # General Information Table
    story.append(Paragraph("<b>General Information</b>", heading_style))
    
    info_data = [
        ["Block ID", str(selected_block)],
    ]
    
    if occurrence_row is not None and not occurrence_row.empty:
        if "Label" in occurrence_row.columns:
            info_data.append(["Actual Label", str(occurrence_row['Label'].iloc[0])])
        if "Type" in occurrence_row.columns:
            info_data.append(["Failure Type", str(occurrence_row['Type'].iloc[0])])
            
    if predicted_label is not None:
        info_data.append(["Predicted Label", str(predicted_label)])
        
    if confidence is not None:
        info_data.append(["Prediction Confidence", f"{float(confidence):.2f}%"])

    info_table = Table(info_data, colWidths=[2.5 * inch, 4 * inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#ECF0F1")),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#2C3E50")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#BDC3C7"))
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))

    # Features Table
    if top10 is not None and not top10.empty:
        story.append(Paragraph("<b>Top Important Features</b>", heading_style))
        
        feature_data = [["Feature Name", "Importance Score"]]
        for _, row in top10.iterrows():
            feature_data.append([str(row['Feature']), f"{row['Importance']:.4f}"])
            
        feature_table = Table(feature_data, colWidths=[3.25 * inch, 3.25 * inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495E")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")])
        ]))
        story.append(feature_table)

    pdf.build(story)
    return Path(output_path).resolve()