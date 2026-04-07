#!/usr/bin/env python3
"""
Analyze images using Gemini vision API for legal case file categorization
"""

import google.generativeai as genai
import os
import sys
from PIL import Image

def analyze_images(image_paths):
    """Analyze images using Gemini vision API"""
    
    # Configure API
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable not set")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    
    # Initialize model - use the model that supports vision
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    results = []
    
    for img_path in image_paths:
        # Convert to absolute path if needed
        if not img_path.startswith('/'):
            img_path = f"/mnt/workspace/{img_path}"
        
        if not os.path.exists(img_path):
            print(f"ERROR: File not found: {img_path}")
            continue
        
        try:
            # Open image
            img = Image.open(img_path)
            
            # Create analysis prompt
            prompt = """Analyze this image for a legal case file organization system.

Client: Michael Deshields
Case: Motor vehicle accident on 10/31/2025

Identify:
1. What type of document/photo is this?
   - Health insurance card (front or back)
   - Driver's license or ID card
   - Accident scene photo
   - Vehicle damage photo
   - Injury photo
   - Other document type

2. Specific details:
   - If insurance card: What carrier name? Is this front or back? Any visible policy numbers?
   - If driver's license: Whose license?
   - If accident/damage photo: Describe what's visible (vehicle type, damage location, scene details)
   - If injury photo: Describe injury location and type
   - Any readable text on the image

3. Proper categorization:
   - "Client" folder - for insurance cards, driver's licenses, personal ID documents
   - "Investigation" folder - for accident scene photos, vehicle damage photos, injury photos

Be specific and detailed in your description."""

            # Generate response
            response = model.generate_content([prompt, img])
            
            filename = os.path.basename(img_path)
            
            print(f"\n{'='*80}")
            print(f"FILE: {filename}")
            print(f"{'='*80}")
            print(response.text)
            print()
            
            results.append({
                "filename": filename,
                "analysis": response.text
            })
            
        except Exception as e:
            print(f"ERROR analyzing {img_path}: {str(e)}")
            continue
    
    # Print summary
    print(f"\n\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Total images analyzed: {len(results)}")
    print()
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_images_with_gemini.py <image1> <image2> ...")
        sys.exit(1)
    
    image_paths = sys.argv[1:]
    analyze_images(image_paths)
