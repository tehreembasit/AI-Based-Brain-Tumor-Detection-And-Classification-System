from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os

def generate_pdf(user, original_img_path, gradcam_path, prediction, confidence):

    # File name
    file_name = f"media/reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # =========================
    # TITLE
    # =========================
    elements.append(Paragraph("Brain Tumor Analysis Report", styles['Title']))
    elements.append(Spacer(1, 20))

    # =========================
    # PATIENT INFO
    # =========================
    patient_data = [
        ["Name", user[1]],
        ["Age", str(user[2])],
        ["Gender", user[3]],
        ["Email", user[4]]
    ]

    table = Table(patient_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(Paragraph("Patient Information", styles['Heading2']))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # =========================
    # MRI IMAGE
    # =========================
    if os.path.exists(original_img_path):
        elements.append(Paragraph("MRI Scan", styles['Heading2']))
        elements.append(Image(original_img_path, width=300, height=300))
        elements.append(Spacer(1, 20))

    # =========================
    # RESULT
    # =========================
    elements.append(Paragraph("Prediction Result", styles['Heading2']))
    elements.append(Paragraph(f"Prediction: {prediction}", styles['Normal']))
    elements.append(Paragraph(f"Confidence: {confidence:.2f}%", styles['Normal']))
    elements.append(Spacer(1, 20))

    # =========================
    # GRAD-CAM
    # =========================
    if os.path.exists(gradcam_path):
        elements.append(Paragraph("Grad-CAM Visualization", styles['Heading2']))
        elements.append(Image(gradcam_path, width=300, height=300))
        elements.append(Spacer(1, 20))

    # =========================
    # DATE & TIME
    # =========================
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generated on: {now}", styles['Normal']))

    # =========================
    # BUILD PDF
    # =========================
    doc.build(elements)

    return file_name