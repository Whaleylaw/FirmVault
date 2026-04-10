
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import pypdf
import os

def create_letter_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    
    Story = []
    
    # Header Info
    header_style = styles["Normal"]
    header_style.fontSize = 11
    header_style.leading = 14
    
    # Date
    Story.append(Paragraph("December 18, 2025", header_style))
    Story.append(Spacer(1, 24))
    
    # Recipient
    Story.append(Paragraph("Araceli Swan", header_style))
    Story.append(Paragraph("Allstar Chiropractic", header_style))
    Story.append(Paragraph("7201 Dixie Hwy", header_style))
    Story.append(Paragraph("Florence, KY 41042", header_style))
    Story.append(Paragraph("Email: aswan@allstar-chiropractic.com", header_style))
    Story.append(Paragraph("Phone: (859) 727-6888", header_style))
    Story.append(Spacer(1, 24))
    
    # Re block
    re_style = ParagraphStyle(name='ReStyle', parent=styles['Normal'], fontName='Helvetica-Bold')
    Story.append(Paragraph("Re: FOLLOW-UP - Medical Records Request", re_style))
    Story.append(Paragraph("Patient: Christopher Lanier", header_style))
    Story.append(Paragraph("Date of Birth: [REDACTED]", header_style))
    Story.append(Paragraph("Date of Incident: June 28, 2025", header_style))
    Story.append(Paragraph("Treatment Dates: June 28, 2025 - December 11, 2025", header_style))
    Story.append(Spacer(1, 24))
    
    # Salutation
    Story.append(Paragraph("Dear Ms. Swan:", header_style))
    Story.append(Spacer(1, 12))
    
    # Body
    body_style = styles["Normal"]
    body_style.fontSize = 11
    body_style.leading = 14
    
    Story.append(Paragraph("This letter serves as a follow-up to our medical records request sent on October 30, 2025 for our client, Christopher Lanier.", body_style))
    Story.append(Spacer(1, 12))
    
    # Request Status
    Story.append(Paragraph("<b>Request Status</b>", body_style))
    Story.append(Paragraph("We understand from your response that you were waiting for the doctor to sign off on the treatment notes. It has now been 49 days since our original request, and we have not yet received the complete medical records.", body_style))
    Story.append(Spacer(1, 12))
    
    # Updated Request
    Story.append(Paragraph("<b>Updated Request</b>", body_style))
    Story.append(Paragraph("Mr. Lanier has completed his treatment as of December 11, 2025. We now request his complete and final medical records, including:", body_style))
    
    bullet_style = ParagraphStyle(name='Bullet', parent=body_style, leftIndent=20)
    bullets = [
        "All office visit notes and treatment records (June 28, 2025 - December 11, 2025)",
        "Complete billing ledger with final itemized charges",
        "All diagnostic imaging reports and results",
        "Any discharge summaries or final treatment reports",
        "All correspondence and referral documentation"
    ]
    for b in bullets:
        Story.append(Paragraph(f"• {b}", bullet_style))
    
    Story.append(Spacer(1, 12))
    
    # Legal Requirements
    Story.append(Paragraph("<b>Legal Requirements</b>", body_style))
    Story.append(Paragraph("Pursuant to KRS 422.317, medical records must be provided within 15 business days of a proper request. Our original request was made 49 days ago, which significantly exceeds the statutory timeframe.", body_style))
    Story.append(Spacer(1, 12))
    
    # Deadline
    Story.append(Paragraph("<b>Deadline</b>", body_style))
    Story.append(Paragraph("We respectfully request that these records be provided by December 27, 2025 (7 business days from today).", body_style))
    Story.append(Spacer(1, 12))
    
    # Authorization
    Story.append(Paragraph("<b>Authorization</b>", body_style))
    Story.append(Paragraph("The signed HIPAA authorization from October 30, 2025 remains valid and is attached to this correspondence for your reference. As required by KRS 422.317, we request these records be provided at no charge as they are being obtained for purposes of supporting a claim or appeal regarding benefits.", body_style))
    Story.append(Spacer(1, 12))
    
    # Contact Information
    Story.append(Paragraph("<b>Contact Information</b>", body_style))
    Story.append(Paragraph("If there are any issues preventing the timely release of these records, please contact our office immediately:", body_style))
    Story.append(Spacer(1, 6))
    Story.append(Paragraph("The Whaley Law Firm, PSC", body_style))
    Story.append(Paragraph("Phone: 502-532-2340", body_style)) # Using a placeholder/injected value if known, but generic for now or "Your Phone"
    Story.append(Paragraph("Email: records@whaleylawfirm.com", body_style)) # Using generic placeholder
    
    Story.append(Spacer(1, 24))
    
    # Closing
    Story.append(Paragraph("We appreciate your prompt attention to this matter and look forward to receiving the complete medical records by the deadline specified above.", body_style))
    Story.append(Spacer(1, 24))
    
    Story.append(Paragraph("Respectfully,", body_style))
    Story.append(Spacer(1, 24))
    
    Story.append(Paragraph("Roscoe", body_style)) # Using Agent Name as requested "Attorney/Paralegal Name"
    Story.append(Paragraph("The Whaley Law Firm, PSC", body_style))
    Story.append(Paragraph("Attorney for Christopher Lanier", body_style))
    
    Story.append(Spacer(1, 24))
    
    Story.append(Paragraph("Enclosure: HIPAA Authorization dated October 30, 2025", header_style))
    Story.append(Paragraph("CC: Justin Chumbley, Attorney", header_style))
    
    doc.build(Story)
    print(f"Created letter at {output_path}")

def combine_pdfs(letter_path, hipaa_path, output_path):
    merger = pypdf.PdfWriter()
    
    # Append letter
    merger.append(letter_path)
    
    # Append HIPAA
    merger.append(hipaa_path)
    
    merger.write(output_path)
    merger.close()
    print(f"Combined PDF saved to {output_path}")

if __name__ == "__main__":
    letter_path = "/tmp/letter.pdf"
    hipaa_path = "/projects/Christopher-Lanier-MVA-6-28-2025/[archive]/Allstar Med Auth.pdf"
    output_path = "/Reports/Christopher_Lanier_Medical_Records_Request_Combined.pdf"
    
    # Ensure tmp directory exists
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
        
    print("Generating Letter...")
    create_letter_pdf(letter_path)
    
    print("Combining PDFs...")
    try:
        combine_pdfs(letter_path, hipaa_path, output_path)
        print("Success!")
    except Exception as e:
        print(f"Error combining PDFs: {e}")
