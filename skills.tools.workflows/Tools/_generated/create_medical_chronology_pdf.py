#!/usr/bin/env python3
"""
Generate PDF Medical Chronology from Markdown
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from datetime import datetime
import sys
from pathlib import Path

def create_medical_chronology_pdf(output_path):
    """Create professional PDF medical chronology"""
    
    # Create PDF
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#7f8c8d'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=HexColor('#667eea'),
        borderPadding=5,
        backColor=HexColor('#f8f9fa')
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#2c3e50'),
        spaceAfter=4,
        leftIndent=20,
        bulletIndent=10
    )
    
    warning_style = ParagraphStyle(
        'Warning',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#856404'),
        spaceAfter=6,
        backColor=HexColor('#fff3cd'),
        borderWidth=1,
        borderColor=HexColor('#ffc107'),
        borderPadding=10,
        borderRadius=5
    )
    
    # Build content
    story = []
    
    # Title Page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("MEDICAL CHRONOLOGY", title_style))
    story.append(Paragraph("Wayne Weber", subtitle_style))
    story.append(Paragraph("Motor Vehicle Accident - January 1, 2022", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Case Information Table
    case_data = [
        ['Client:', 'Wayne Weber'],
        ['Date of Birth:', 'July 13, 1947'],
        ['Age at MVA:', '74 years'],
        ['Date of Accident:', 'January 1, 2022'],
        ['Accident Type:', 'Motor Vehicle Accident (T-boned on driver side)'],
        ['Report Date:', datetime.now().strftime('%B %d, %Y')]
    ]
    
    case_table = Table(case_data, colWidths=[2*inch, 4*inch])
    case_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(case_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Confidentiality Notice
    story.append(Paragraph(
        "<b>CONFIDENTIAL - ATTORNEY WORK PRODUCT</b><br/>"
        "Prepared in anticipation of litigation. Not for distribution.",
        ParagraphStyle('Confidential', parent=body_style, alignment=TA_CENTER, textColor=HexColor('#e74c3c'))
    ))
    
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("EXECUTIVE SUMMARY", heading2_style))
    story.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Total Visits Documented:', '9 visits'],
        ['Date Range:', 'January 1, 2022 to August 18, 2023'],
        ['Pre-MVA Visits:', '0 documented'],
        ['Post-MVA Visits:', '9'],
        ['MVA-Related Visits:', '5'],
        ['Unrelated Visits:', '3 (diabetes management, toe amputation)']
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    # MVA-Related Diagnoses
    story.append(Paragraph("<b>MVA-Related Diagnoses:</b>", body_style))
    diagnoses = [
        "Right 8th and 9th rib fractures (minimally displaced)",
        "Right shoulder pain/injury",
        "Supraspinatus and infraspinatus tendinopathy",
        "Severe AC joint arthritis (likely pre-existing, aggravated by MVA)",
        "Contusion of head",
        "Chest wall pain"
    ]
    for dx in diagnoses:
        story.append(Paragraph(f"• {dx}", bullet_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Pre-existing Conditions
    story.append(Paragraph("<b>Pre-Existing Conditions:</b>", body_style))
    conditions = [
        "Type 2 Diabetes Mellitus",
        "Hypertension",
        "Hyperlipidemia",
        "Vitamin B12 deficiency",
        "History of DVT/PE",
        "Sleep apnea",
        "Status post left total hip arthroplasty",
        "History of appendectomy"
    ]
    for cond in conditions:
        story.append(Paragraph(f"• {cond}", bullet_style))
    
    story.append(PageBreak())
    
    # Red Flags Section
    story.append(Paragraph("🚨 CRITICAL RED FLAGS", heading2_style))
    story.append(Spacer(1, 0.1*inch))
    
    red_flags = [
        ("<b>6.5-Month Treatment Gap:</b>", "MVA occurred 01/01/2022. Shoulder pain began 01/02/2022. First shoulder evaluation: 07/26/2022. This significant delay may complicate causation argument."),
        ("<b>Severe Pre-Existing Shoulder Pathology:</b>", "MRI showed severe AC joint arthritis, glenohumeral osteoarthritis, degenerative labral tear, and enchondroma. These findings suggest significant pre-existing degenerative changes that pre-date the MVA."),
        ("<b>Inconsistent Accident Descriptions:</b>", "EMS reported 'minimal damage' and 10 mph impact. Sports Medicine documented 'Jaws of Life used to extract.' This discrepancy needs resolution."),
        ("<b>Incomplete Follow-Up:</b>", "Patient wanted shoulder injections (08/23/2022) but no documented follow-up visits occurred after August 2022. Lack of continued treatment may weaken claim."),
        ("<b>No PIP Benefits Paid:</b>", "Despite auto insurance coverage, $0.00 PIP benefits paid. May indicate carrier denied MVA-related treatment."),
        ("<b>Pattern of Non-Compliance:</b>", "Patient failed to return for follow-up for 2 months after toe amputation surgery, suggesting possible non-compliance with medical care.")
    ]
    
    for title, description in red_flags:
        story.append(Paragraph(f"{title} {description}", warning_style))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # Complete Chronology
    story.append(Paragraph("COMPLETE MEDICAL CHRONOLOGY", heading2_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Visit 1: EMS
    story.append(Paragraph("January 1, 2022 - Anchorage Middletown Fire EMS", heading3_style))
    story.append(Paragraph("<b>Time:</b> 18:03-19:09 | <b>Type:</b> Emergency Medical Services | <b>MVA-Related:</b> Yes", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Chief Complaint:</b> Right rib pain following motor vehicle accident", body_style))
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>Incident Details:</b>", body_style))
    ems_details = [
        "Location: LaGrange Rd at I-265N",
        "Vehicle: All-Terrain Vehicle/Moped",
        "Mechanism: T-boned on driver's side",
        "Damage: Minimal to driver side",
        "Speed: Estimated 10 mph",
        "Weather: Rain",
        "Patient ambulatory at scene"
    ]
    for detail in ems_details:
        story.append(Paragraph(f"• {detail}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Assessment:</b> Alert and oriented x4, no visible injury, complained of right rib palpation pain, no LOC, vital signs stable (BP: 186/77, Pulse: 77, SpO2: 99%), GCS: 15", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Diagnoses:</b> Injury (general), intercostal pain, motorized vehicle accident", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Treatment:</b> ALS assessment, transported to Norton Brownsboro Hospital", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Visit 2: Norton ER
    story.append(Paragraph("January 1, 2022 - Norton Brownsboro Hospital Emergency Department", heading3_style))
    story.append(Paragraph("<b>Time:</b> 18:36-23:04 | <b>Type:</b> Emergency Department Visit | <b>MVA-Related:</b> Yes", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Chief Complaint:</b> Motor vehicle crash (car hit driver door), right rib pain, closed head injury", body_style))
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>History:</b> 74 y/o male with history of hyperlipidemia, diabetes, previous DVT/PE. Restrained driver, T-boned on driver side. No LOC. Head busted out window. Left arm jabbed ribs. No rib step-off, no SOB, no abdominal/neck/back pain.", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Imaging Results:</b>", body_style))
    imaging = [
        "<b>CT Head Without Contrast:</b> No acute intracranial abnormality. Moderate ischemic white matter disease. Chronic left maxillary sinusitis.",
        "<b>Chest X-Ray:</b> <font color='#e74c3c'><b>Minimally displaced fractures of right 8th and 9th ribs.</b></font> No pneumothorax."
    ]
    for img in imaging:
        story.append(Paragraph(f"• {img}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Diagnoses:</b> (1) Motor vehicle accident, initial encounter (2) Contusion of head (3) Chest wall pain", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Treatment:</b> No medications given. Patient monitored and observed.", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Disposition:</b> Discharged home in good condition. Follow up with PCP (Dr. Davidson).", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Treatment Gap Warning
    story.append(Paragraph(
        "⚠️ 6.5 MONTH TREATMENT GAP - Patient reported shoulder pain began 01/02/2022 but did not seek treatment until 07/26/2022",
        warning_style
    ))
    story.append(Spacer(1, 0.3*inch))
    
    # Visit 3: Internal Medicine (Unrelated)
    story.append(Paragraph("July 14, 2022 - Baptist Health Medical Group Internal Medicine", heading3_style))
    story.append(Paragraph("<b>Provider:</b> Sarah C. Dorf, APRN | <b>Type:</b> Office Visit | <b>MVA-Related:</b> No (routine chronic disease management)", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Chief Complaint:</b> Hypotension", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Diagnoses:</b> Type 2 diabetes, B12 deficiency, hypertension, hyperlipidemia, chronic right shoulder pain (noted on problem list)", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<i>Note: Chronic right shoulder pain mentioned but no specific MVA discussion. This visit occurred 6.5 months after MVA.</i>", ParagraphStyle('Italic', parent=body_style, textColor=HexColor('#7f8c8d'))))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    
    # Visit 4: Sports Medicine
    story.append(Paragraph("July 26, 2022 - Baptist Health Medical Group Sports Medicine", heading3_style))
    story.append(Paragraph("<b>Provider:</b> Christopher V. Pitcock, MD | <b>Type:</b> New Patient Evaluation | <b>MVA-Related:</b> Yes", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Chief Complaint:</b> Shoulder pain after going through windshield in MVA January 1st", body_style))
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>History:</b> Patient was T-boned, head went through driver-side window, jammed between door and steering wheel. <b>EMS used Jaws of Life to extract him.</b> ER showed rib fractures. <font color='#e74c3c'><b>Day after accident, patient began having right shoulder pain.</b></font> Has continued to have pain since. No prior treatments. Pain over right superior lateral shoulder, worse with overhead motions.", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Physical Exam Findings:</b>", body_style))
    exam_findings = [
        "Palpable arthrosis over AC joint (non-tender)",
        "Tenderness to palpation of subacromial space",
        "<b>Positive Neer test</b> (impingement)",
        "<b>Positive Hawkins test</b> (impingement)",
        "<b>Positive empty can test</b> (supraspinatus weakness)",
        "Equivocal drop arm test",
        "Decreased external rotation by ~10°",
        "Decreased internal rotation by 5-10°"
    ]
    for finding in exam_findings:
        story.append(Paragraph(f"• {finding}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>In-Office X-Ray Findings:</b> Severe AC arthritis, Hill-Sachs appearing lesion, mild OA changes, high riding humeral head", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Assessment:</b> Injury of right shoulder, initial encounter", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Plan:</b> MRI shoulder ordered. Concerned for rotator cuff tear. Follow-up after MRI.", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Visit 5: MRI
    story.append(Paragraph("August 19, 2022 - Baptist Health Eastpoint MRI", heading3_style))
    story.append(Paragraph("<b>Ordering Provider:</b> Christopher V. Pitcock, MD | <b>Type:</b> MRI Imaging | <b>MVA-Related:</b> Yes", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Procedure:</b> MRI Shoulder Right Without Contrast", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Indication:</b> Shoulder pain, rotator cuff disorder suspected, shoulder trauma", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>MRI FINDINGS:</b>", body_style))
    mri_findings = [
        "<b>Rotator Cuff:</b> Intermediate T2 signal in supraspinatus and infraspinatus tendons = <b>tendinopathy</b>. No rotator cuff tear. No retraction or atrophy.",
        "<b>AC Joint:</b> <font color='#e74c3c'><b>Advanced AC joint arthritis</b></font> with exuberant bony overgrowth, chronic ossification, small effusion, acromial spur.",
        "<b>Glenohumeral Joint:</b> <font color='#e74c3c'><b>Mild-to-moderate osteoarthritis</b></font>, glenoid marginal spurs, <b>degenerative tear of posterior-superior labrum</b>, articular cartilage thinning.",
        "<b>Bone:</b> Lobular lesion in proximal humerus (8 cm) - likely <b>enchondroma</b> (benign cartilage tumor)."
    ]
    for finding in mri_findings:
        story.append(Paragraph(f"• {finding}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Impression:</b> (1) Diffuse supraspinatus and infraspinatus tendinopathy without tear (2) Severe AC joint arthritis (3) Mild-to-moderate glenohumeral OA with degenerative labral tear (4) Nonaggressive bone lesion (enchondroma)", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Radiologist:</b> Dr. Gregory Elliott, MD", body_style))
    
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        "⚠️ <b>CAUSATION CONCERN:</b> MRI shows significant pre-existing degenerative changes (severe AC arthritis, glenohumeral OA, labral tear) that pre-date the MVA. However, tendinopathy could have been aggravated by trauma.",
        warning_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Visit 6: Phone Call
    story.append(Paragraph("August 23, 2022 - Baptist Health Medical Group Sports Medicine", heading3_style))
    story.append(Paragraph("<b>Staff:</b> Carley Wright, MA | <b>Type:</b> Telephone Encounter | <b>MVA-Related:</b> Yes", body_style))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Contact:</b> Patient's brother called regarding MRI results", body_style))
    story.append(Spacer(1, 0.05*inch))
    
    story.append(Paragraph("<b>Discussion:</b>", body_style))
    discussion = [
        "Brother asked if results due to old age or accident",
        "<font color='#27ae60'><b>Medical assistant stated: 'It looked like the arthritis was there previous to the accident and that the accident probably aggravated it'</b></font>",
        "Patient wants to proceed with injections",
        "Will call back to schedule appointment"
    ]
    for item in discussion:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "✓ <b>FAVORABLE EVIDENCE:</b> Medical staff acknowledged accident 'probably aggravated' pre-existing arthritis - supports aggravation claim.",
        ParagraphStyle('Success', parent=body_style, textColor=HexColor('#27ae60'), backColor=HexColor('#e8f5e9'), borderWidth=1, borderColor=HexColor('#27ae60'), borderPadding=8)
    ))
    
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "⚠️ <b>RED FLAG:</b> No documented follow-up visit occurred after this call despite patient wanting injections.",
        warning_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    # No Further Shoulder Treatment Warning
    story.append(Paragraph(
        "⚠️ NO DOCUMENTED SHOULDER TREATMENT AFTER AUGUST 2022 - Patient wanted injections but no follow-up visits documented",
        warning_style
    ))
    
    story.append(PageBreak())
    
    # Unrelated Visits
    story.append(Paragraph("UNRELATED MEDICAL VISITS", heading2_style))
    story.append(Paragraph("<i>(Included for completeness - not related to MVA)</i>", ParagraphStyle('Italic', parent=body_style, textColor=HexColor('#7f8c8d'), alignment=TA_CENTER)))
    story.append(Spacer(1, 0.2*inch))
    
    # Visit 7: Lab Review
    story.append(Paragraph("November 4, 2022 - Baptist Health Medical Group Internal Medicine", heading3_style))
    story.append(Paragraph("<b>Provider:</b> Sarah C. Dorf, APRN | <b>Type:</b> Lab Results Review | <b>MVA-Related:</b> No", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Purpose:</b> Follow-up for lab results (routine chronic disease management)", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Key Findings:</b> Anemia identified (low RBC, hemoglobin, hematocrit). Diabetes not well controlled (A1c 7.6%). Additional testing ordered.", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Visit 8: Toe Amputation
    story.append(Paragraph("June 20, 2023 - Baptist Health LaGrange (Vascular Surgery)", heading3_style))
    story.append(Paragraph("<b>Surgeon:</b> David A. Lipski, MD | <b>Type:</b> Inpatient Surgery | <b>MVA-Related:</b> No", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Diagnoses:</b> (1) Osteomyelitis of distal phalanx of left great toe (2) Diabetes with diabetic neuropathy", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Procedure:</b> Amputation of distal phalanx of left great toe", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Outcome:</b> Procedure tolerated well, no complications, prognosis for healing: very good", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<i>Note: Completely unrelated to MVA - diabetic foot complication</i>", ParagraphStyle('Italic', parent=body_style, textColor=HexColor('#7f8c8d'))))
    story.append(Spacer(1, 0.3*inch))
    
    # Visit 9: Vascular Follow-up
    story.append(Paragraph("August 18, 2023 - Baptist Health Vascular Surgery", heading3_style))
    story.append(Paragraph("<b>Provider:</b> Emily Hickerson, NP | <b>Type:</b> Follow-up Visit | <b>MVA-Related:</b> No", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Chief Complaint:</b> Arterial evaluation - cutaneous ulcers on right foot", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>History:</b> Follow-up after left great toe amputation (6/20/2023). <font color='#e74c3c'><b>Patient did not return for follow-up for almost 2 months</b></font> - sutures in place for 2 months. Now presenting with new breakdown on right foot.", body_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph("<b>Assessment:</b> Likely pressure ulcer from neuropathy and ill-fitting shoes. X-ray ordered to rule out osteomyelitis.", body_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "⚠️ <b>RED FLAG:</b> Patient failed to return for 2-month follow-up after surgery, suggesting possible pattern of non-compliance.",
        warning_style
    ))
    
    story.append(PageBreak())
    
    # Summary & Analysis
    story.append(Paragraph("SUMMARY & ANALYSIS", heading2_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Timeline of MVA-Related Treatment:</b>", body_style))
    story.append(Spacer(1, 0.1*inch))
    timeline_summary = [
        "<b>01/01/2022:</b> MVA occurs, immediate EMS transport and ER evaluation",
        "<b>01/01/2022:</b> Diagnosed with rib fractures and head contusion, discharged home",
        "<b>01/02/2022:</b> Patient reports shoulder pain began (day after MVA)",
        "<font color='#e74c3c'><b>6.5 MONTH GAP - NO TREATMENT</b></font>",
        "<b>07/26/2022:</b> First evaluation of shoulder pain by Sports Medicine",
        "<b>08/19/2022:</b> MRI performed showing tendinopathy and severe pre-existing arthritis",
        "<b>08/23/2022:</b> Phone call discussing MRI results, patient wants injections",
        "<font color='#e74c3c'><b>NO DOCUMENTED FOLLOW-UP AFTER AUGUST 2022</b></font>"
    ]
    for item in timeline_summary:
        story.append(Paragraph(f"• {item}", bullet_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Strengths
    story.append(Paragraph("<b>CASE STRENGTHS:</b>", body_style))
    story.append(Spacer(1, 0.05*inch))
    strengths = [
        "Clear mechanism of injury (T-boned, head through window)",
        "Immediate medical attention (EMS and ER same day)",
        "Objective findings (rib fractures on x-ray)",
        "Temporal relationship (shoulder pain began day after accident)",
        "Medical acknowledgment (staff noted accident 'probably aggravated' arthritis)",
        "Positive physical exam findings (impingement signs, reduced ROM)"
    ]
    for strength in strengths:
        story.append(Paragraph(f"✓ {strength}", bullet_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Weaknesses
    story.append(Paragraph("<b>CASE WEAKNESSES:</b>", body_style))
    story.append(Spacer(1, 0.05*inch))
    weaknesses = [
        "Significant treatment gap (6.5 months between MVA and shoulder evaluation)",
        "Pre-existing pathology (severe AC arthritis, glenohumeral OA, labral tear)",
        "Incomplete treatment (no follow-up after August 2022 despite wanting injections)",
        "Inconsistent accident descriptions (minimal damage vs. Jaws of Life)",
        "Unrelated medical issues (diabetic foot complications)",
        "Low-speed impact (estimated 10 mph, minimal vehicle damage)",
        "No PIP payments (despite auto insurance, $0.00 paid)",
        "Possible non-compliance (failed 2-month follow-up after toe amputation)"
    ]
    for weakness in weaknesses:
        story.append(Paragraph(f"✗ {weakness}", bullet_style))
    
    story.append(PageBreak())
    
    # Causation Analysis
    story.append(Paragraph("CAUSATION ANALYSIS", heading2_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Rib Fractures:</b>", body_style))
    story.append(Paragraph("Clear causation - documented immediately after MVA on chest x-ray, consistent with mechanism of injury (T-bone impact, left arm jabbing ribs). <font color='#27ae60'><b>Strong causation.</b></font>", body_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Shoulder Injury:</b>", body_style))
    story.append(Paragraph("More complex. <b>Aggravation of pre-existing condition</b> is most supportable argument. MRI shows severe pre-existing degenerative changes (AC arthritis, glenohumeral OA, labral tear). However, tendinopathy could have been caused or worsened by trauma. Medical staff acknowledged accident 'probably aggravated' the arthritis. Positive impingement signs and reduced ROM support injury. <font color='#e74c3c'><b>But 6.5-month treatment gap significantly weakens causation argument.</b></font>", body_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    story.append(Paragraph("RECOMMENDATIONS", heading2_style))
    story.append(Spacer(1, 0.1*inch))
    
    recommendations = [
        "Obtain complete medical records from all providers to identify any missing visits",
        "Depose treating providers to establish opinions on causation and aggravation",
        "Consider orthopedic expert to opine on whether trauma could cause/aggravate tendinopathy",
        "Address treatment gap - obtain explanation from client for delay in seeking treatment",
        "Clarify accident details - resolve inconsistencies in mechanism descriptions (Jaws of Life vs. minimal damage)",
        "Document current status - is patient still having shoulder pain? Any treatment since August 2022?",
        "Consider settlement value carefully given pre-existing conditions and treatment gaps",
        "Investigate PIP denial - determine why no benefits were paid"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        story.append(Paragraph(f"{i}. {rec}", bullet_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    story.append(Paragraph(
        f"<b>Prepared by:</b> Whaley Law Firm, PSC<br/>"
        f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>"
        f"<b>Case:</b> Wayne Weber MVA - 01/01/2022<br/><br/>"
        f"<b>CONFIDENTIAL - ATTORNEY WORK PRODUCT</b>",
        ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER, textColor=HexColor('#7f8c8d'), fontSize=9)
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created: {output_path}")

def main():
    # Determine workspace root
    workspace = Path("/workspace")
    if not workspace.exists():
        workspace = Path("/mnt/workspace")
    
    output_path = workspace / "projects" / "Wayne-Weber-MVA-01-01-2022" / "Reports" / "Medical_Chronology_Wayne_Weber.pdf"
    
    create_medical_chronology_pdf(output_path)

if __name__ == "__main__":
    main()
