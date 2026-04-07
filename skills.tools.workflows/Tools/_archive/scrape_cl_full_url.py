#!/usr/bin/env python3
"""
Scrape CourtListener docket page from full URL
"""
import sys
import json
import requests
from bs4 import BeautifulSoup
import re

def scrape_docket_url(url):
    """Scrape docket entries from CourtListener URL"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Fetching: {url}", file=sys.stderr)
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}", file=sys.stderr)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract case information
        case_info = {
            'url': url,
            'case_name': '',
            'case_number': '',
            'court': '',
            'date_filed': '',
            'judge': ''
        }
        
        # Try to find case title
        title_elem = soup.find('h2', class_='bottom')
        if not title_elem:
            title_elem = soup.find('h1')
        if title_elem:
            case_info['case_name'] = title_elem.get_text(strip=True)
        
        # Find case metadata
        for dt in soup.find_all('dt'):
            label = dt.get_text(strip=True).lower()
            dd = dt.find_next_sibling('dd')
            if dd:
                value = dd.get_text(strip=True)
                if 'case number' in label or 'docket number' in label:
                    case_info['case_number'] = value
                elif 'court' in label:
                    case_info['court'] = value
                elif 'filed' in label:
                    case_info['date_filed'] = value
                elif 'judge' in label or 'assigned to' in label:
                    case_info['judge'] = value
        
        # Find docket entries
        entries = []
        
        # Look for table rows with docket entries
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 3:
                # Try to extract entry number, date, and description
                entry_num = cols[0].get_text(strip=True)
                date_text = cols[1].get_text(strip=True)
                desc_text = ' '.join([col.get_text(strip=True) for col in cols[2:]])
                
                # Only add if looks like a valid entry
                if entry_num and (entry_num.isdigit() or re.match(r'\d+', entry_num)):
                    entry = {
                        'docket_number': entry_num,
                        'date': date_text,
                        'description': desc_text
                    }
                    entries.append(entry)
        
        # Alternative: Look for specific docket entry divs/sections
        if not entries:
            for elem in soup.find_all(['div', 'p'], class_=re.compile(r'docket|entry')):
                text = elem.get_text(strip=True)
                if text and len(text) > 10:
                    # Try to parse entry
                    match = re.match(r'(\d+)\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+(.+)', text)
                    if match:
                        entries.append({
                            'docket_number': match.group(1),
                            'date': match.group(2),
                            'description': match.group(3)
                        })
        
        result = {
            'success': True,
            'case_info': case_info,
            'entries': entries,
            'total_entries': len(entries),
            'html_length': len(response.text)
        }
        
        print(json.dumps(result, indent=2))
        return result
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__,
            'url': url
        }
        print(json.dumps(error_result, indent=2))
        return error_result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scrape_cl_full_url.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scrape_docket_url(url)
