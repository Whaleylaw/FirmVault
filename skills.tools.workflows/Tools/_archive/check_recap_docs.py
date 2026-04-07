#!/usr/bin/env python3
"""
Check CourtListener for downloadable PDFs from RECAP archive
"""
import requests
import json
import sys

def check_recap_availability(docket_id):
    """
    Check if documents are available for download from RECAP
    """
    # CourtListener docket page
    base_url = f"https://www.courtlistener.com/docket/{docket_id}/robinson-v-eastern-express-inc/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Checking RECAP availability for docket {docket_id}...")
    print(f"URL: {base_url}\n")
    
    # Note: CourtListener provides free access to documents in RECAP archive
    # Documents NOT in RECAP require PACER purchase
    
    print("=" * 80)
    print("DOCUMENT AVAILABILITY ANALYSIS")
    print("=" * 80)
    print()
    print("CourtListener provides two types of document access:")
    print()
    print("1. ✅ FREE - RECAP Archive Documents")
    print("   - Documents previously purchased from PACER by RECAP users")
    print("   - Available for free download from CourtListener")
    print("   - Look for 'Download PDF' links on docket page")
    print()
    print("2. 💰 PAID - PACER-Only Documents")
    print("   - Not yet in RECAP archive")
    print("   - Require purchase from PACER ($0.10/page, max $3.00/document)")
    print("   - CourtListener shows 'Buy on PACER' button")
    print()
    print("=" * 80)
    print("HOW TO ACCESS DOCUMENTS")
    print("=" * 80)
    print()
    print("Option 1: Check CourtListener Directly")
    print(f"   Visit: {base_url}")
    print("   - Look for blue 'Download PDF' buttons (FREE - in RECAP)")
    print("   - Look for 'Buy on PACER' buttons (PAID - not in RECAP)")
    print()
    print("Option 2: Use PACER Directly")
    print("   1. Go to: https://pacer.uscourts.gov/")
    print("   2. Search for case: 3:23-cv-00048-GFVT-EBA")
    print("   3. Download docket sheet and documents")
    print("   4. Cost: ~$0.10/page (max $3.00 per document)")
    print()
    print("Option 3: Request via RECAP Extension")
    print("   - Install RECAP browser extension")
    print("   - When you view documents on PACER, RECAP auto-uploads to archive")
    print("   - Makes documents free for everyone in the future")
    print()
    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print()
    print("1. Visit CourtListener page to see which docs are in RECAP (free)")
    print("2. For docs not in RECAP, use PACER (typically $5-15 total for full docket)")
    print("3. Install RECAP extension to contribute back to free archive")
    print()
    print(f"Direct link: {base_url}")
    print()

if __name__ == '__main__':
    docket_id = "68422564"
    check_recap_availability(docket_id)
