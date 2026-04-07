#!/usr/bin/env python3
"""
Combine multiple PDFs into a single PDF file.
Can also convert markdown to PDF first, then combine.

Usage:
    python combine_pdfs.py output.pdf input1.pdf input2.pdf [input3.pdf ...]
    python combine_pdfs.py output.pdf --markdown input.md input2.pdf
"""

import sys
import os
from pathlib import Path

try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("ERROR: PyPDF2 not installed. Installing now...")
    os.system("pip install PyPDF2")
    from PyPDF2 import PdfMerger

try:
    import markdown
    from weasyprint import HTML
    MARKDOWN_SUPPORT = True
except ImportError:
    MARKDOWN_SUPPORT = False
    print("WARNING: markdown and/or weasyprint not installed.")
    print("Markdown conversion not available. Install with:")
    print("  pip install markdown weasyprint")


def markdown_to_pdf(md_path, pdf_path):
    """Convert markdown file to PDF."""
    if not MARKDOWN_SUPPORT:
        print("ERROR: Markdown support not available. Install dependencies:")
        print("  pip install markdown weasyprint")
        sys.exit(1)
    
    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Add basic styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 0 20px;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=styled_html).write_pdf(pdf_path)
    print(f"✓ Converted {md_path} to PDF")


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
    print(f"  Total pages from {len(input_paths)} files")


def main():
    if len(sys.argv) < 3:
        print("Usage: python combine_pdfs.py output.pdf input1.pdf input2.pdf [...]")
        print("   or: python combine_pdfs.py output.pdf --markdown input.md input2.pdf")
        sys.exit(1)
    
    output_path = sys.argv[1]
    inputs = sys.argv[2:]
    
    # Check for markdown conversion
    temp_pdfs = []
    pdf_inputs = []
    
    for i, input_path in enumerate(inputs):
        if input_path == "--markdown":
            continue
        
        # Check if previous arg was --markdown flag
        if i > 0 and inputs[i-1] == "--markdown":
            # Convert markdown to PDF
            temp_pdf = input_path.replace('.md', '_temp.pdf')
            markdown_to_pdf(input_path, temp_pdf)
            pdf_inputs.append(temp_pdf)
            temp_pdfs.append(temp_pdf)
        else:
            # Regular PDF
            pdf_inputs.append(input_path)
    
    # Combine all PDFs
    combine_pdfs(output_path, pdf_inputs)
    
    # Clean up temp files
    for temp_pdf in temp_pdfs:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
            print(f"Cleaned up: {temp_pdf}")


if __name__ == "__main__":
    main()
