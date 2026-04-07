#!/usr/bin/env python3
"""
Analyze and rename JPG images in Clarence Robinson case folder
Uses OCR to identify document content and generate proper filenames
"""

from PIL import Image
import pytesseract
import os
import re
from datetime import datetime
import json

case_root = "/workspace/projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021"

def extract_text_from_image(img_path):
    """Extract text from image using OCR"""
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"ERROR: {str(e)}"

def find_dates(text):
    """Find dates in text"""
    dates = []
    
    # Pattern: MM/DD/YYYY or MM-DD-YYYY
    pattern1 = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b'
    matches1 = re.findall(pattern1, text)
    for m, d, y in matches1:
        try:
            date_obj = datetime(int(y), int(m), int(d))
            dates.append(date_obj.strftime('%Y-%m-%d'))
        except:
            pass
    
    # Pattern: Month DD, YYYY
    pattern2 = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})\b'
    matches2 = re.findall(pattern2, text, re.IGNORECASE)
    for month, day, year in matches2:
        try:
            date_obj = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
            dates.append(date_obj.strftime('%Y-%m-%d'))
        except:
            pass
    
    return dates

def classify_document(text, filename):
    """Classify document type based on OCR text"""
    text_lower = text.lower()
    
    # Medical Records - FCE
    if any(word in text_lower for word in ['functional capacity', 'fce', 'physical capacity', 'max safe lift']):
        return 'Medical Records', 'FCE'
    
    # Medical Records - PT
    if any(word in text_lower for word in ['physical therapy', 'benchmark', 'range of motion', 'therapeutic']):
        return 'Medical Records', 'Physical Therapy'
    
    # Medical Records - Work Restrictions
    if any(word in text_lower for word in ['work restriction', 'return to work', 'work release', 'work notice']):
        return 'Medical Records', 'Work Restriction'
    
    # Medical Records - Prescription
    if any(word in text_lower for word in ['prescription', 'rx', 'pharmacy', 'medication']):
        return 'Medical Records', 'Prescription'
    
    # Medical Records - General
    if any(word in text_lower for word in ['medical report', 'doctor', 'physician', 'patient', 'diagnosis']):
        return 'Medical Records', 'Medical Report'
    
    # Expenses - Check
    if any(word in text_lower for word in ['check', 'pay to the order', 'bank', 'routing number']):
        return 'Expenses', 'Payment Check'
    
    # Default
    return 'Unknown', 'Unknown Document'

def analyze_all_images():
    """Analyze all JPG images in case root"""
    
    # Get all JPG files in root only (not subdirectories)
    all_files = os.listdir(case_root)
    jpg_files = [f for f in all_files if f.lower().endswith('.jpg') and os.path.isfile(os.path.join(case_root, f))]
    
    print(f"🔍 Found {len(jpg_files)} JPG images to analyze\n")
    print("=" * 80)
    
    results = []
    
    for i, jpg_file in enumerate(sorted(jpg_files), 1):
        print(f"\n[{i}/{len(jpg_files)}] Analyzing: {jpg_file}")
        
        img_path = os.path.join(case_root, jpg_file)
        
        # Extract text
        text = extract_text_from_image(img_path)
        
        if text.startswith("ERROR"):
            print(f"  ❌ {text}")
            results.append({
                'old_name': jpg_file,
                'new_name': None,
                'category': 'ERROR',
                'doc_type': 'ERROR',
                'date': None,
                'confidence': 0,
                'reason': text
            })
            continue
        
        # Find dates
        dates = find_dates(text)
        best_date = dates[0] if dates else '2021-06-10'  # Default to accident date
        
        # Classify document
        category, doc_type = classify_document(text, jpg_file)
        
        # Generate new filename
        if category != 'Unknown':
            # Create description from doc_type and filename hints
            description = doc_type
            
            # Add page number if it's a numbered scan
            if jpg_file.startswith('01.114688-'):
                page_num = jpg_file.split('-')[1]
                description = f"{doc_type} Page {page_num}"
            
            new_name = f"{best_date} - Clarence Robinson - {category} - {description}.jpg"
            confidence = 'HIGH' if dates and category != 'Unknown' else 'MEDIUM'
        else:
            new_name = f"UNKNOWN - {jpg_file}"
            confidence = 'LOW'
        
        # Show preview of OCR text
        preview = text[:200].replace('\n', ' ')
        print(f"  📄 OCR Preview: {preview}...")
        print(f"  📅 Date found: {best_date}")
        print(f"  📁 Category: {category}")
        print(f"  📝 Type: {doc_type}")
        print(f"  ✨ New name: {new_name}")
        print(f"  🎯 Confidence: {confidence}")
        
        results.append({
            'old_name': jpg_file,
            'new_name': new_name,
            'category': category,
            'doc_type': doc_type,
            'date': best_date,
            'confidence': confidence,
            'ocr_preview': preview,
            'full_text': text
        })
    
    # Save results to JSON
    results_file = os.path.join(case_root, "Reports", "image_analysis_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"\n✅ Analysis complete! Results saved to:")
    print(f"   {results_file}")
    
    # Summary
    categories = {}
    for r in results:
        cat = r['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 SUMMARY:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} files")
    
    return results

if __name__ == "__main__":
    results = analyze_all_images()
