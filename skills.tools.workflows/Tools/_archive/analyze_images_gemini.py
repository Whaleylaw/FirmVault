#!/usr/bin/env python3
"""
Gemini Vision API Image Analysis Tool for Case Files
Analyzes images using Google's Gemini vision model for detailed categorization
"""

import sys
import os
from pathlib import Path

try:
    import google.generativeai as genai
    from PIL import Image
except ImportError:
    print("ERROR: Required libraries not installed.")
    print("Install with: pip install google-generativeai Pillow")
    sys.exit(1)

def analyze_image_with_gemini(image_path, model):
    """Analyze an image using Gemini vision API"""
    try:
        # Open image
        img = Image.open(image_path)
        
        # Analyze with Gemini
        prompt = """Analyze this image for a legal case file organization system.

Identify:
1. What type of document/photo is this?
   - Health insurance card (front/back)
   - Driver's license or ID
   - Accident scene photo
   - Vehicle damage photo
   - Injury photo
   - Other

2. Specific details:
   - If insurance card: What carrier? Front or back?
   - If accident/damage: Describe what's visible
   - If injury: Describe injury location
   - Any text visible on the image

3. Proper categorization:
   - Client folder (for insurance cards, IDs)
   - Investigation folder (for accident/damage/injury photos)

Be specific and detailed."""

        response = model.generate_content([prompt, img])
        
        return {
            "filename": os.path.basename(image_path),
            "path": image_path,
            "analysis": response.text,
            "success": True
        }
    except Exception as e:
        return {
            "filename": os.path.basename(image_path),
            "path": image_path,
            "error": str(e),
            "success": False
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_images_gemini.py <image_path> [image_path2] ...")
        print("\nExample:")
        print("  python analyze_images_gemini.py /path/to/image1.jpg /path/to/image2.jpg")
        sys.exit(1)
    
    # Configure Gemini API
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable not set")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    
    # Initialize model
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
    except Exception as e:
        print(f"ERROR: Failed to initialize Gemini model: {e}")
        sys.exit(1)
    
    # Process each image
    results = []
    for image_path in sys.argv[1:]:
        if not os.path.exists(image_path):
            print(f"ERROR: File not found: {image_path}")
            continue
        
        print(f"\nAnalyzing: {os.path.basename(image_path)}...")
        result = analyze_image_with_gemini(image_path, model)
        results.append(result)
        
        # Print result
        print(f"\n{'='*80}")
        print(f"FILE: {result['filename']}")
        print(f"{'='*80}")
        
        if result['success']:
            print(result['analysis'])
        else:
            print(f"ERROR: {result['error']}")
    
    # Print summary
    print(f"\n\n{'='*80}")
    print("ANALYSIS SUMMARY")
    print(f"{'='*80}\n")
    print(f"Total images analyzed: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r['success'])}")
    print(f"Failed: {sum(1 for r in results if not r['success'])}")
    
    print(f"\n{'='*80}")
    print("FILES PROCESSED")
    print(f"{'='*80}\n")
    for r in results:
        status = "✓" if r['success'] else "✗"
        print(f"{status} {r['filename']}")

if __name__ == "__main__":
    main()
