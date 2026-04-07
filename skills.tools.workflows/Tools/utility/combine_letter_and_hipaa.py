#!/usr/bin/env python3
"""
Combine a markdown letter with a HIPAA PDF authorization.
Converts markdown to PDF, then merges with HIPAA PDF.

Usage:
    python combine_letter_and_hipaa.py letter.md hipaa.pdf output.pdf
"""

import sys
import os
import subprocess
from pathlib import Path

# Check for required packages and install if needed
try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("Installing PyPDF2...")
    subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"], check=True)
    from PyPDF2 import PdfMerger

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError:
    print("Installing reportlab...")
    subprocess.run([sys.executable, "-m", "pip", "install", "reportlab"], check=True)
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER


def markdown_to_pdf_simple(md_path, pdf_path):
    """Convert markdown to PDF using reportlab."""
    
    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=1*inch, rightMargin=1*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='#2c3e50',
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor='#34495e',
        spaceAfter=6,
        spaceBefore=12,
        bold=True
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=6
    )
    
    # Parse markdown and build story
    story = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Title (# heading)
        if line.startswith('# '):
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
        
        # Heading (## heading)
        elif line.startswith('## '):
            text = line[3:].strip()
            story.append(Paragraph(text, heading_style))
        
        # Bold (**text**)
        elif line.startswith('**') and line.endswith('**'):
            text = line[2:-2].strip()
            story.append(Paragraph(f"<b>{text}</b>", body_style))
        
        # Horizontal rule
        elif line.startswith('---'):
            story.append(Spacer(1, 0.2*inch))
        
        # Bullet points
        elif line.startswith('- '):
            text = line[2:].strip()
            # Handle checkmarks
            text = text.replace('✅ ', '• ')
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{text}", body_style))
        
        # Regular text
        else:
            # Handle bold inline
            text = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            story.append(Paragraph(text, body_style))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Converted {md_path} to PDF: {pdf_path}")


def combine_pdfs(output_path, input_paths):
    """Combine multiple PDFs into one."""
    merger = PdfMerger()
    
    for pdf_path in input_paths:
        if not os.path.exists(pdf_path):
            print(f"ERROR: File not found: {pdf_path}")
            sys.exit(1)
        
        print(f"Adding: {pdf_path}")
        merger.append(pdf_path)
    
    # Write combined PDF
    merger.write(output_path)
    merger.close()
    
    print(f"\n✓ Combined PDF created: {output_path}")
    print(f"  Contains {len(input_paths)} documents")


def main():
    if len(sys.argv) != 4:
        print("Usage: python combine_letter_and_hipaa.py letter.md hipaa.pdf output.pdf")
        sys.exit(1)
    
    letter_md = sys.argv[1]
    hipaa_pdf = sys.argv[2]
    output_pdf = sys.argv[3]
    
    # Check files exist
    if not os.path.exists(letter_md):
        print(f"ERROR: Letter file not found: {letter_md}")
        sys.exit(1)
    
    if not os.path.exists(hipaa_pdf):
        print(f"ERROR: HIPAA file not found: {hipaa_pdf}")
        sys.exit(1)
    
    # Convert letter to PDF
    temp_letter_pdf = letter_md.replace('.md', '_temp.pdf')
    markdown_to_pdf_simple(letter_md, temp_letter_pdf)
    
    # Combine PDFs
    combine_pdfs(output_pdf, [temp_letter_pdf, hipaa_pdf])
    
    # Clean up temp file
    if os.path.exists(temp_letter_pdf):
        os.remove(temp_letter_pdf)
        print(f"Cleaned up temporary file: {temp_letter_pdf}")
    
    print(f"\n✅ SUCCESS! Combined document ready: {output_pdf}")


if __name__ == "__main__":
    main()
