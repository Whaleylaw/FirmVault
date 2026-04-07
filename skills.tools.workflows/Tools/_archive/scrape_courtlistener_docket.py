#!/usr/bin/env python3
"""
Scrape CourtListener docket page using requests and BeautifulSoup
"""
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_docket(docket_id):
    """Scrape docket entries from CourtListener"""
    url = f"https://www.courtlistener.com/docket/{docket_id}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract case information
        case_info = {}
        case_info['url'] = url
        
        # Try to find case title
        title_elem = soup.find('h1')
        if title_elem:
            case_info['case_name'] = title_elem.get_text(strip=True)
        
        # Find docket entries table
        entries = []
        
        # Look for docket entry rows
        docket_table = soup.find('table', {'id': 'docket-entry-table'}) or soup.find('table', class_='docket-entry-table')
        
        if docket_table:
            rows = docket_table.find_all('tr')
            for row in rows[1:]:  # Skip header
                cols = row.find_all('td')
                if len(cols) >= 3:
                    entry = {
                        'docket_number': cols[0].get_text(strip=True),
                        'date': cols[1].get_text(strip=True),
                        'description': cols[2].get_text(strip=True)
                    }
                    entries.append(entry)
        
        # Alternative: look for div-based entries
        if not entries:
            entry_divs = soup.find_all('div', class_='docket-entry')
            for div in entry_divs:
                entry = {}
                num_elem = div.find(class_='entry-number')
                date_elem = div.find(class_='entry-date')
                desc_elem = div.find(class_='entry-description')
                
                if num_elem:
                    entry['docket_number'] = num_elem.get_text(strip=True)
                if date_elem:
                    entry['date'] = date_elem.get_text(strip=True)
                if desc_elem:
                    entry['description'] = desc_elem.get_text(strip=True)
                
                if entry:
                    entries.append(entry)
        
        result = {
            'success': True,
            'case_info': case_info,
            'entries': entries,
            'total_entries': len(entries)
        }
        
        print(json.dumps(result, indent=2))
        return result
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'url': url
        }
        print(json.dumps(error_result, indent=2))
        return error_result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scrape_courtlistener_docket.py <docket_id>")
        sys.exit(1)
    
    docket_id = sys.argv[1]
    scrape_docket(docket_id)
