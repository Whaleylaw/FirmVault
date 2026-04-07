#!/usr/bin/env python3
"""
Extract error rate from quality review summary.

Usage:
    python get_error_rate.py <summary_file>

Arguments:
    summary_file: Path to quality review summary markdown file

Output:
    JSON with error rate and recommendation
"""

import argparse
import json
import re
import sys
from pathlib import Path


def get_error_rate(summary_file: str) -> dict:
    """Extract error rate from quality review summary."""
    path = Path(summary_file)
    
    if not path.exists():
        return {"error": f"File not found: {summary_file}", "success": False}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to find error rate in various formats
        error_rate = None
        
        # Pattern 1: "Error Rate: X%" or "error rate: X%"
        match = re.search(r'[Ee]rror [Rr]ate[:\s]+(\d+(?:\.\d+)?)\s*%', content)
        if match:
            error_rate = float(match.group(1))
        
        # Pattern 2: "X% error rate"
        if error_rate is None:
            match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*error rate', content, re.IGNORECASE)
            if match:
                error_rate = float(match.group(1))
        
        # Pattern 3: "errors: X/Y" and calculate
        if error_rate is None:
            match = re.search(r'[Ee]rrors?[:\s]+(\d+)\s*/\s*(\d+)', content)
            if match:
                errors = int(match.group(1))
                total = int(match.group(2))
                if total > 0:
                    error_rate = (errors / total) * 100
        
        # Pattern 4: Look for "X files flagged" and "Y total files"
        if error_rate is None:
            flagged_match = re.search(r'(\d+)\s*files?\s*flagged', content, re.IGNORECASE)
            total_match = re.search(r'(\d+)\s*total\s*files?', content, re.IGNORECASE)
            if flagged_match and total_match:
                flagged = int(flagged_match.group(1))
                total = int(total_match.group(1))
                if total > 0:
                    error_rate = (flagged / total) * 100
        
        if error_rate is None:
            return {
                "success": False,
                "error": "Could not extract error rate from summary",
                "file": summary_file
            }
        
        # Determine recommendation
        if error_rate <= 20:
            recommendation = "PROCEED - Main agent review of flagged files"
            action = "review_flagged"
        else:
            recommendation = "RETRY or ESCALATE - Error rate too high"
            action = "retry_or_escalate"
        
        return {
            "success": True,
            "file": summary_file,
            "error_rate": round(error_rate, 2),
            "threshold": 20,
            "below_threshold": error_rate <= 20,
            "recommendation": recommendation,
            "action": action
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def main():
    parser = argparse.ArgumentParser(description="Extract error rate from quality review")
    parser.add_argument("summary_file", help="Path to quality review summary")
    args = parser.parse_args()
    
    result = get_error_rate(args.summary_file)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()

