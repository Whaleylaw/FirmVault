#!/usr/bin/env python3
"""
Convert Medical Chronology Markdown to PDF using weasyprint
"""

import sys
from pathlib import Path

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("❌ weasyprint not available")
    print("Creating HTML version instead...")
    sys.exit(1)

def markdown_to_html(md_content):
    """Convert markdown to styled HTML"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: letter;
            margin: 0.75in;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #7f8c8d;
            }}
        }}
        
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #2c3e50;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 24pt;
            text-align: center;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #2c3e50;
            font-size: 16pt;
            margin-top: 20pt;
            margin-bottom: 12pt;
            background-color: #f8f9fa;
            padding: 8pt;
            border-left: 4pt solid #667eea;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 14pt;
            margin-top: 15pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #34495e;
            font-size: 11pt;
            margin-top: 10pt;
            margin-bottom: 6pt;
            font-weight: bold;
        }}
        
        p {{
            margin-bottom: 8pt;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 20pt;
            margin-bottom: 10pt;
        }}
        
        li {{
            margin-bottom: 4pt;
        }}
        
        .case-info {{
            text-align: center;
            color: #7f8c8d;
            font-size: 12pt;
            margin-bottom: 30pt;
        }}
        
        .warning {{
            background-color: #fff3cd;
            border: 2pt solid #ffc107;
            padding: 12pt;
            margin: 15pt 0;
            border-radius: 5pt;
            color: #856404;
        }}
        
        .success {{
            background-color: #e8f5e9;
            border: 2pt solid #27ae60;
            padding: 12pt;
            margin: 15pt 0;
            border-radius: 5pt;
            color: #27ae60;
        }}
        
        .red-flag {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .favorable {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        hr {{
            border: none;
            border-top: 2pt solid #dee2e6;
            margin: 20pt 0;
        }}
        
        .confidential {{
            text-align: center;
            color: #e74c3c;
            font-weight: bold;
            margin: 20pt 0;
            padding: 10pt;
            border: 2pt solid #e74c3c;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
"""
    
    # Convert markdown content to HTML
    # Simple conversion - replace markdown syntax with HTML
    lines = md_content.split('\n')
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += "<p>&nbsp;</p>\n"
            continue
        
        # Headers
        if line.startswith('# '):
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith('## '):
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith('### '):
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += f"<h3>{line[4:]}</h3>\n"
        elif line.startswith('#### '):
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += f"<h4>{line[5:]}</h4>\n"
        # Horizontal rule
        elif line.startswith('---'):
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += "<hr/>\n"
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html += "<ul>\n"
                in_list = True
            content = line[2:]
            # Bold
            content = content.replace('**', '<b>').replace('**', '</b>')
            html += f"<li>{content}</li>\n"
        # Numbered lists
        elif len(line) > 2 and line[0].isdigit() and line[1] == '.':
            if in_list:
                html += "</ul>\n"
                in_list = False
            content = line[line.index('.')+1:].strip()
            content = content.replace('**', '<b>').replace('**', '</b>')
            html += f"<p><b>{line[:line.index('.')+1]}</b> {content}</p>\n"
        # Regular paragraph
        else:
            if in_list:
                html += "</ul>\n"
                in_list = False
            # Bold
            line = line.replace('**', '<b>', 1)
            if '**' in line:
                line = line.replace('**', '</b>', 1)
            html += f"<p>{line}</p>\n"
    
    if in_list:
        html += "</ul>\n"
    
    html += """
</body>
</html>
"""
    
    return html

def main():
    # Determine workspace root
    workspace = Path("/workspace")
    if not workspace.exists():
        workspace = Path("/mnt/workspace")
    
    md_path = workspace / "projects" / "Wayne-Weber-MVA-01-01-2022" / "Reports" / "Medical_Chronology_Wayne_Weber.md"
    pdf_path = workspace / "projects" / "Wayne-Weber-MVA-01-01-2022" / "Reports" / "Medical_Chronology_Wayne_Weber.pdf"
    
    # Read markdown
    with open(md_path, 'r') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown_to_html(md_content)
    
    # Create PDF
    font_config = FontConfiguration()
    HTML(string=html_content).write_pdf(pdf_path, font_config=font_config)
    
    print(f"✅ PDF created: {pdf_path}")

if __name__ == "__main__":
    main()
