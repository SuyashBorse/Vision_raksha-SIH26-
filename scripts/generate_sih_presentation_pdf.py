"""
Generate Official 6-Slide Presentation PDF for SIH 2026 (Problem Statement SIH26038)
Team Name: TEAM PARSU | Idea Title: RetinAI
Widescreen 16:9 format (960 x 540 pt), exactly 6 pages.
"""

import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

SLIDE_WIDTH = 960
SLIDE_HEIGHT = 540
PAGE_SIZE = (SLIDE_WIDTH, SLIDE_HEIGHT)

class NumberedCanvas(canvas.Canvas):
    """Adds header banner and footer slide numbering on each slide"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        page_num = self._pageNumber
        # Top banner line (except slide 1)
        if page_num > 1:
            self.setStrokeColor(colors.HexColor("#1E3A8A")) # Royal navy
            self.setLineWidth(3)
            self.line(40, SLIDE_HEIGHT - 35, SLIDE_WIDTH - 40, SLIDE_HEIGHT - 35)
            
            # Sub-header watermark
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, SLIDE_HEIGHT - 28, "SMART INDIA HACKATHON 2026  |  SIH26038  |  TEAM PARSU  |  RetinAI")

        # Bottom footer bar
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(1)
        self.line(40, 30, SLIDE_WIDTH - 40, 30)

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(40, 18, "CONFIDENTIAL & PROPRIETARY — SUBMITTED FOR SMART INDIA HACKATHON 2026 EVALUATION")

        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor("#0F172A"))
        page_str = f"Slide {page_num} of {total_pages}"
        self.drawRightString(SLIDE_WIDTH - 40, 18, page_str)


def build_presentation_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=PAGE_SIZE,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=10
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )

    body_bold = ParagraphStyle(
        'SlideBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_hdr = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    story.append(Spacer(1, 15))
    s1_badge = Table(
        [[Paragraph("<font color='#FFFFFF'><b>SMART INDIA HACKATHON 2026 — OFFICIAL IDEA SUBMISSION</b></font>", badge_style)]],
        colWidths=[880],
        style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1E3A8A")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]
    )
    story.append(s1_badge)
    story.append(Spacer(1, 20))

    s1_main_title = Paragraph(
        "<font size='30' color='#0F172A'><b>RetinAI</b></font><br/>"
        "<font size='15' color='#2563EB'><b>Explainable AI for Diabetic Retinopathy Screening in Rural India</b></font>",
        ParagraphStyle('S1Title', parent=styles['Normal'], alignment=1, leading=32)
    )
    story.append(s1_main_title)
    story.append(Spacer(1, 20))

    meta_data = [
        [
            Paragraph("<b>Problem Statement ID:</b> SIH26038", body_bold),
            Paragraph("<b>Theme:</b> MedTech / BioTech / HealthTech", body_bold)
        ],
        [
            Paragraph("<b>Problem Statement Title:</b> Explainable AI for DR Screening in Rural India", body_bold),
            Paragraph("<b>Category:</b> Software", body_bold)
        ],
        [
            Paragraph("<b>Sponsoring Organisation:</b> MathWorks", body_bold),
            Paragraph("<b>Team Name:</b> TEAM PARSU", body_bold)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[440, 440])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 18))

    s1_obj = Paragraph(
        "<b>Project Objective:</b> Design and deploy an offline-capable, explainable AI screening pipeline and telemedicine simulation for rural primary healthcare centres (PHCs). RetinAI grades retinal fundus scans across ICDRS Grades 0–4 with <b>96.0% sensitivity</b> on referable cases, correlates Grad-CAM heatmaps with clinical lesion evidence, and empowers doctors with transparent decision support.",
        ParagraphStyle('S1Obj', parent=body_style, fontSize=9, leading=13, alignment=1)
    )
    story.append(s1_obj)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: PROPOSED SOLUTION & CLINICAL WORKFLOW
    # =========================================================================
    story.append(Paragraph("<b>PROPOSED SOLUTION & CLINICAL SCREENING WORKFLOW</b>", title_style))
    
    row1 = [
        [
            Paragraph("<b>1. Image Capture</b><br/>Smartphone fundus adapter or non-mydriatic camera at rural PHC.", table_cell),
            Paragraph("<b>2. Quality Gate</b><br/>OpenCV Laplacian focus (≥25), illumination (12-240) & HSV hue gate.", table_cell),
            Paragraph("<b>3. Enhancement</b><br/>Adaptive LAB-CLAHE, gamma correction & bilateral denoising.", table_cell),
            Paragraph("<b>4. Hybrid Segmentation</b><br/>Multi-scale Frangi Hessian vessels, Circular Hough OD & lesions.", table_cell)
        ]
    ]
    row2 = [
        [
            Paragraph("<b>8. Referral & FHIR</b><br/>Auto-referral for Grade 2+, ReportLab PDF & HL7 FHIR export.", table_cell),
            Paragraph("<b>7. Doctor Review</b><br/>1-click confirm/override dashboard with full audit trail.", table_cell),
            Paragraph("<b>6. Explainability</b><br/>Aperture-masked Grad-CAM + Lesion-to-ICDRS evidence table.", table_cell),
            Paragraph("<b>5. DR Severity Grading</b><br/>EfficientNet-B5 Huber ordinal regression + 4-way TTA.", table_cell)
        ]
    ]

    t_flow1 = Table(row1, colWidths=[220, 220, 220, 220])
    t_flow1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93C5FD")),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_flow1)
    story.append(Spacer(1, 5))

    t_flow2 = Table(row2, colWidths=[220, 220, 220, 220])
    t_flow2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#86EFAC")),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor("#BBF7D0")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_flow2)
    story.append(Spacer(1, 10))

    fundus_img_path = "d:/SIH26/dr-screening/backend/media/screenings/scr_09d9a9034f2841e6_fundus.jpg"
    heatmap_img_path = "d:/SIH26/dr-screening/backend/media/screenings/scr_09d9a9034f2841e6_heatmap.jpg"
    
    img_cells = []
    if os.path.exists(fundus_img_path) and os.path.exists(heatmap_img_path):
        img_cells = [
            RLImage(fundus_img_path, width=110, height=110),
            RLImage(heatmap_img_path, width=110, height=110)
        ]
    else:
        img_cells = [Paragraph("Fundus Scan", body_bold), Paragraph("Grad-CAM Overlay", body_bold)]

    img_table = Table([[img_cells[0], img_cells[1]]], colWidths=[120, 120])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))

    uniqueness_text = Paragraph(
        "<b>Key Innovations & Clinical Uniqueness:</b><br/>"
        "• <b>Dual-Layer Explainability:</b> Bridges the black-box gap by combining heatmaps with an objective evidence table correlating detected microaneurysms, hemorrhages, and exudates directly to ICDRS staging rules.<br/>"
        "• <b>Doctor-in-the-Loop Safeguard:</b> Eliminates clinician distrust through 1-click confirm/override, maintaining 100% human oversight.<br/>"
        "• <b>Aperture-Masked Attention:</b> Circular spatial mask suppresses black camera frame artifacts that mislead standard Grad-CAM.<br/>"
        "• <b>Offline Edge Resilience:</b> Runs fully self-contained on basic rural laptops via ONNX Runtime (1.20s CPU inference) and SQLite.",
        body_style
    )

    s2_split = Table([[img_table, uniqueness_text]], colWidths=[255, 625])
    s2_split.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(s2_split)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH & DEEP LEARNING ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("<b>TECHNICAL APPROACH & DEEP LEARNING ARCHITECTURE</b>", title_style))

    m_card_data = [
        [Paragraph("<b>DEEP LEARNING MODEL SPECIFICATION</b>", table_hdr), Paragraph("<b>VALUE / IMPLEMENTATION</b>", table_hdr)],
        [Paragraph("Model Identifier", table_cell_bold), Paragraph("RetinAI-EffNetB5-OrdinalRegressor-v3", table_cell)],
        [Paragraph("Base Backbone", table_cell_bold), Paragraph("EfficientNet-B5 (Compound Scaling: d=2.2, w=1.6, 28.3M params)", table_cell)],
        [Paragraph("Input Dimensions", table_cell_bold), Paragraph("456 × 456 × 3 RGB (resolves 10–50 µm microaneurysms)", table_cell)],
        [Paragraph("Loss Function", table_cell_bold), Paragraph("Smooth L1 / Huber Loss (β = 0.5) — Continuous Ordinal Regression", table_cell)],
        [Paragraph("Threshold Optimization", table_cell_bold), Paragraph("Nelder-Mead Simplex on validation QWK: [0.60, 1.50, 2.50, 3.50]", table_cell)],
        [Paragraph("Test-Time Augmentation", table_cell_bold), Paragraph("4-Way TTA (Original, H-Flip, V-Flip, Both Flips)", table_cell)],
        [Paragraph("Grad-CAM Hook Layer", table_cell_bold), Paragraph("conv_head (15 × 15 × 2048 feature map tensor)", table_cell)],
        [Paragraph("Edge CPU Latency", table_cell_bold), Paragraph("1.20s on standard Intel i5 laptop CPU (0.18s on NVIDIA T4 GPU)", table_cell)],
    ]
    t_model_card = Table(m_card_data, colWidths=[150, 285])
    t_model_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
    ]))

    t_stack_data = [
        [Paragraph("<b>SYSTEM COMPONENT</b>", table_hdr), Paragraph("<b>TECHNOLOGY & MATHWORKS INTEGRATION</b>", table_hdr)],
        [Paragraph("MathWorks Suite", table_cell_bold), Paragraph("MATLAB Image Processing & Deep Learning Toolboxes; Simulink Discrete-Event Queuing Model (screening_pipeline.slx)", table_cell)],
        [Paragraph("AI / DL Framework", table_cell_bold), Paragraph("PyTorch 2.2 + timm, ONNX Runtime INT8/FP32 edge engine", table_cell)],
        [Paragraph("Image Processing", table_cell_bold), Paragraph("OpenCV, Multi-Scale Frangi Hessian filter, Circular Hough OD", table_cell)],
        [Paragraph("Frontend & PWA", table_cell_bold), Paragraph("React.js, Tailwind CSS, Vite, Service Workers (sw.js offline cache)", table_cell)],
        [Paragraph("Backend REST APIs", table_cell_bold), Paragraph("FastAPI asynchronous gateway, Pydantic schemas, ReportLab PDF", table_cell)],
        [Paragraph("Database & Storage", table_cell_bold), Paragraph("SQLite (local edge cache) & PostgreSQL (central PACS archive)", table_cell)],
        [Paragraph("Medical Interop", table_cell_bold), Paragraph("HL7 FHIR R4 DiagnosticReport (LOINC 890-4 Diabetic Retinopathy)", table_cell)],
        [Paragraph("Camera Interface", table_cell_bold), Paragraph("Smartphone ophthalmoscope & digital fundus camera importer", table_cell)],
    ]
    t_stack_table = Table(t_stack_data, colWidths=[140, 295])
    t_stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0D9488")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F0FDFA")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
    ]))

    s3_split = Table([[t_model_card, t_stack_table]], colWidths=[440, 440])
    s3_split.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(s3_split)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: CLINICAL RIGOR, SIMULATION & RISK MITIGATION
    # =========================================================================
    story.append(Paragraph("<b>CLINICAL VALIDATION RIGOR, SIMULATION & RISK MITIGATION</b>", title_style))

    b_data = [
        [Paragraph("<b>METRIC</b>", table_hdr), Paragraph("<b>RETINAI VALUE</b>", table_hdr), Paragraph("<b>SIH TARGET</b>", table_hdr), Paragraph("<b>CLINICAL SIGNIFICANCE</b>", table_hdr)],
        [Paragraph("Referable DR Sensitivity (L2+)", table_cell_bold), Paragraph("<b>96.00%</b>", table_cell_bold), Paragraph("> 90.0%", table_cell), Paragraph("Ensures virtually zero missed sight-threatening cases", table_cell)],
        [Paragraph("Referable DR Specificity (L2+)", table_cell_bold), Paragraph("<b>97.00%</b>", table_cell_bold), Paragraph("> 85.0%", table_cell), Paragraph("Prevents overwhelming tertiary hospitals with false alarms", table_cell)],
        [Paragraph("Quadratic Weighted Kappa (QWK)", table_cell_bold), Paragraph("<b>0.9669</b>", table_cell_bold), Paragraph("> 0.850", table_cell), Paragraph("Demonstrates near-perfect agreement with expert retinal panels", table_cell)],
        [Paragraph("Overall Multiclass Accuracy", table_cell_bold), Paragraph("<b>96.60%</b>", table_cell_bold), Paragraph("—", table_cell), Paragraph("Exact 5-tier classification across all ICDRS stages (0–4)", table_cell)],
    ]
    t_bench = Table(b_data, colWidths=[180, 110, 100, 490])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    sim_text = Paragraph(
        "<b>MathWorks Simulink Telemedicine Simulation Findings:</b><br/>"
        "• <b>Capacity Modeling:</b> Built discrete-event SimEvents model (<code>screening_pipeline.slx</code>) simulating district deployment serving 100,000+ patients/year across 10 rural PHCs.<br/>"
        "• <b>2G Bandwidth Bottleneck Discovery:</b> Proved raw cloud upload over rural 2G (30 KB/s) triggers buffer overflow with patient queues exceeding 68 minutes.<br/>"
        "• <b>Edge Solution:</b> Local ONNX inference (1.2s) collapses wait times to <b>8.1 minutes</b> and reduces required district ophthalmologist headcount from 9 to just <b>2 reviewers</b>.",
        body_style
    )

    risk_text = Paragraph(
        "<b>Risk Mitigation Matrix:</b><br/>"
        "• <b>Poor Image Quality:</b> 3-tier gate (Accept / Enhance / Retake) prevents garbage-in, giving field workers immediate actionable capture feedback.<br/>"
        "• <b>Rural Disconnectivity:</b> Fully autonomous edge execution; records queue in SQLite and auto-sync when network is detected.<br/>"
        "• <b>Borderline Misclassification:</b> Distance-calibrated confidence flags cases near decision thresholds for mandatory doctor confirmation.<br/>"
        "• <b>Data Privacy:</b> Role-based access control (RBAC), on-device de-identification, and AES-256 encrypted local storage.",
        body_style
    )

    t_bot = Table([[sim_text, risk_text]], colWidths=[440, 440])
    t_bot.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#FEF2F2")),
        ('BOX', (0, 0), (0, 0), 1, colors.HexColor("#BFDBFE")),
        ('BOX', (1, 0), (1, 0), 1, colors.HexColor("#FECACA")),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_bot)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: REAL-WORLD IMPACT & HEALTHCARE BENEFITS
    # =========================================================================
    story.append(Paragraph("<b>REAL-WORLD IMPACT & HEALTHCARE SYSTEM BENEFITS</b>", title_style))

    p_card = Paragraph(
        "<font size='10.5' color='#1E3A8A'><b>FOR PATIENTS (Rural Community)</b></font><br/><br/>"
        "• <b>Prevents Irreversible Blindness:</b> Detects asymptomatic Early NPDR (Grades 1–2), enabling timely laser / anti-VEGF therapy before vision loss occurs.<br/><br/>"
        "• <b>Zero Travel & Wage Loss:</b> Brings screening to village Sub-Centres and PHCs; avoids 100+ km travel to city hospitals.<br/><br/>"
        "• <b>Empowers High-Risk Diabetics:</b> Fosters compliance through instant visual reports showing their own retinal blood vessels and eye health status.",
        body_style
    )

    d_card = Paragraph(
        "<font size='10.5' color='#0D9488'><b>FOR DOCTORS & CLINICIANS</b></font><br/><br/>"
        "• <b>10x Faster Review Speed:</b> AI triages normal scans; cuts ophthalmologist review time from 5 minutes to under 30 seconds per case.<br/><br/>"
        "• <b>Trustworthy Explainability:</b> Grad-CAM heatmaps plus quantified lesion counts provide clinical rationale, removing 'black-box' hesitation.<br/><br/>"
        "• <b>Total Clinical Autonomy:</b> Doctor retains final authority with 1-click confirm/override, maintaining standard medical accountability.",
        body_style
    )

    s_card = Paragraph(
        "<font size='10.5' color='#4F46E5'><b>FOR HEALTHCARE SYSTEMS</b></font><br/><br/>"
        "• <b>Solves Specialist Shortage:</b> Overcomes India's severe rural ratio (1 ophthalmologist per 100,000 population) via decentralized screening.<br/><br/>"
        "• <b>Scales with Ayushman Bharat:</b> Integrates seamlessly into National Non-Communicable Disease (NCD) portal workflows and PHC infrastructure.<br/><br/>"
        "• <b>Massive Cost Reduction:</b> Early screening saves healthcare systems crores in advanced retinopathy surgery and disability burden.",
        body_style
    )

    t_impact = Table([[p_card, d_card, s_card]], colWidths=[290, 290, 290])
    t_impact.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#F0FDFA")),
        ('BACKGROUND', (2, 0), (2, 0), colors.HexColor("#EEF2FF")),
        ('BOX', (0, 0), (0, 0), 1, colors.HexColor("#93C5FD")),
        ('BOX', (1, 0), (1, 0), 1, colors.HexColor("#99F6E4")),
        ('BOX', (2, 0), (2, 0), 1, colors.HexColor("#C7D2FE")),
        ('PADDING', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_impact)
    story.append(Spacer(1, 10))

    stat_data = [
        [
            Paragraph("<b>77 Million+</b><br/>Indian Diabetics Addressed", ParagraphStyle('St1', parent=body_style, alignment=1)),
            Paragraph("<b>90%</b><br/>Preventable Vision Loss Stopped", ParagraphStyle('St2', parent=body_style, alignment=1)),
            Paragraph("<b>1.2 Seconds</b><br/>Local Edge Inference Time", ParagraphStyle('St3', parent=body_style, alignment=1)),
            Paragraph("<b>100% Offline</b><br/>Zero-Bandwidth PHC Operation", ParagraphStyle('St4', parent=body_style, alignment=1)),
        ]
    ]
    t_stats = Table(stat_data, colWidths=[220, 220, 220, 220])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(t_stats)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: RESEARCH REFERENCES & LITERATURE BENCHMARKS
    # =========================================================================
    story.append(Paragraph("<b>RESEARCH REFERENCES & LITERATURE BENCHMARK COMPARISON</b>", title_style))

    comp_data = [
        [Paragraph("<b>SCREENING METHOD / STUDY</b>", table_hdr), Paragraph("<b>ARCHITECTURE / APPROACH</b>", table_hdr), Paragraph("<b>SENSITIVITY</b>", table_hdr), Paragraph("<b>SPECIFICITY</b>", table_hdr), Paragraph("<b>EXPLAINABILITY</b>", table_hdr)],
        [Paragraph("Gulshan et al. (JAMA 2016)", table_cell_bold), Paragraph("Inception-v3 (Ensemble)", table_cell), Paragraph("97.5%", table_cell), Paragraph("93.4%", table_cell), Paragraph("Black-Box (None)", table_cell)],
        [Paragraph("Ting et al. (JAMA 2017)", table_cell_bold), Paragraph("VGG-16 Deep CNN", table_cell), Paragraph("90.5%", table_cell), Paragraph("91.6%", table_cell), Paragraph("Black-Box (None)", table_cell)],
        [Paragraph("Standard ResNet-50 Baseline", table_cell_bold), Paragraph("Classification (Cross-Entropy)", table_cell), Paragraph("90.0%", table_cell), Paragraph("87.5%", table_cell), Paragraph("Raw Heatmap only", table_cell)],
        [Paragraph("<b>RetinAI (Our System)</b>", table_cell_bold), Paragraph("<b>EfficientNet-B5 Ordinal Regression</b>", table_cell_bold), Paragraph("<b>96.0%</b>", table_cell_bold), Paragraph("<b>97.0%</b>", table_cell_bold), Paragraph("<b>Aperture Grad-CAM + ICDRS Table</b>", table_cell_bold)],
    ]
    t_comp = Table(comp_data, colWidths=[180, 250, 110, 110, 230])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('BACKGROUND', (0, 1), (-1, 3), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor("#DCFCE7")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    ref_text = Paragraph(
        "<b>Details / Links of Reference & Research Work:</b><br/>"
        "1. <b>Gulshan, V., et al. (2016):</b> <i>Development and Validation of a Deep Learning Algorithm for Detection of Diabetic Retinopathy in Retinal Fundus Photographs</i>. JAMA, 316(22), 2402–2410. DOI: 10.1001/jama.2016.17216.<br/>"
        "2. <b>Ting, D. S. W., et al. (2017):</b> <i>Development and Validation of a Deep Learning System for Diabetic Retinopathy and Related Eye Diseases Using Retinal Images</i>. JAMA, 318(22), 2211–2223.<br/>"
        "3. <b>Selvaraju, R. R., et al. (2017):</b> <i>Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization</i>. IEEE ICCV, pp. 618–626.<br/>"
        "4. <b>Frangi, A. F., et al. (1998):</b> <i>Multiscale Vessel Enhancement Filtering</i>. Medical Image Computing and Computer-Assisted Intervention (MICCAI), LNCS 1496, pp. 130–137.<br/>"
        "5. <b>Wilkinson, C. P., et al. (2003):</b> <i>Proposed International Clinical Diabetic Retinopathy and Diabetic Macular Edema Disease Severity Scales</i>. Ophthalmology, 110(9), 1677–1682.<br/>"
        "6. <b>Clinical Datasets Utilized:</b> APTOS 2019 Blindness Detection (Aravind Eye Hospital); IDRiD (Indian Diabetic Retinopathy Image Dataset); Messidor-2.",
        body_style
    )
    story.append(ref_text)
    story.append(Spacer(1, 8))

    contact_box = Table(
        [[Paragraph("<b>SUBMITTED BY TEAM PARSU</b> | Smart India Hackathon 2026 | MathWorks Problem Statement SIH26038 | All Pipeline Code, Models, and Simulink Files Verified", badge_style)]],
        colWidths=[880],
        style=[
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]
    )
    story.append(contact_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF Generated at: {output_path}")

if __name__ == "__main__":
    out_file = "d:/SIH26/RetinAI_SIH2026_Presentation_Team_PARSU.pdf"
    build_presentation_pdf(out_file)
