#!/usr/bin/env python3
"""
Image Analysis Tool for Case Files
Analyzes images and provides descriptions for categorization
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("ERROR: Required libraries not installed. Install with: pip install Pillow pytesseract")
    sys.exit(1)

def analyze_image(image_path):
    """Analyze an image and extract text/metadata"""
    try:
        img = Image.open(image_path)
        
        # Get basic image info
        width, height = img.size
        format_type = img.format
        mode = img.mode
        
        # Try to extract text using OCR
        try:
            text = pytesseract.image_to_string(img)
            text = text.strip()
        except Exception as e:
            text = f"OCR failed: {str(e)}"
        
        return {
            "path": image_path,
            "filename": os.path.basename(image_path),
            "dimensions": f"{width}x{height}",
            "format": format_type,
            "mode": mode,
            "extracted_text": text[:500] if text else "No text detected",  # First 500 chars
            "has_text": len(text) > 10 if text else False
        }
    except Exception as e:
        return {
            "path": image_path,
            "filename": os.path.basename(image_path),
            "error": str(e)
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_images.py <image_path> [image_path2] ...")
        sys.exit(1)
    
    results = []
    for image_path in sys.argv[1:]:
        if not os.path.exists(image_path):
            print(f"ERROR: File not found: {image_path}")
            continue
        
        result = analyze_image(image_path)
        results.append(result)
        
        # Print result
        print(f"\n{'='*60}")
        print(f"File: {result['filename']}")
        print(f"Path: {result.get('path', 'N/A')}")
        if 'error' in result:
            print(f"ERROR: {result['error']}")
        else:
            print(f"Dimensions: {result['dimensions']}")
            print(f"Format: {result['format']}")
            print(f"Mode: {result['mode']}")
            print(f"Has Text: {result['has_text']}")
            print(f"\nExtracted Text Preview:")
            print("-" * 60)
            print(result['extracted_text'])
            print("-" * 60)

if __name__ == "__main__":
    main()
