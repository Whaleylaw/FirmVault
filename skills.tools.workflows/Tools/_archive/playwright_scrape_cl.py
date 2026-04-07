#!/usr/bin/env python3
"""
Scrape CourtListener docket using Playwright for dynamic content
"""
import sys
import json
import asyncio
from playwright.async_api import async_playwright
import re

async def scrape_docket_playwright(url):
    """Scrape docket using Playwright"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print(f"Loading: {url}", file=sys.stderr)
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Wait for content to load
            await page.wait_for_timeout(3000)
            
            # Extract case information
            case_info = {
                'url': url,
                'case_name': '',
                'case_number': '',
                'court': '',
                'date_filed': '',
                'judge': ''
            }
            
            # Get page title
            title = await page.title()
            case_info['page_title'] = title
            
            # Extract case name from h2 or h1
            case_name_elem = await page.query_selector('h2.bottom, h1')
            if case_name_elem:
                case_info['case_name'] = await case_name_elem.inner_text()
            
            # Get all text content
            content = await page.content()
            
            # Extract docket entries
            entries = []
            
            # Look for table rows
            rows = await page.query_selector_all('table tr, tbody tr')
            
            for row in rows:
                cells = await row.query_selector_all('td')
                if len(cells) >= 3:
                    cell_texts = []
                    for cell in cells:
                        text = await cell.inner_text()
                        cell_texts.append(text.strip())
                    
                    # Check if first cell looks like entry number
                    if cell_texts[0] and (cell_texts[0].isdigit() or re.match(r'\d+', cell_texts[0])):
                        entry = {
                            'docket_number': cell_texts[0],
                            'date': cell_texts[1] if len(cell_texts) > 1 else '',
                            'description': ' '.join(cell_texts[2:]) if len(cell_texts) > 2 else ''
                        }
                        entries.append(entry)
            
            # If no entries found in table, try alternative selectors
            if not entries:
                # Look for any element with docket entry pattern
                all_text = await page.inner_text('body')
                lines = all_text.split('\n')
                
                for line in lines:
                    # Pattern: number date description
                    match = re.match(r'^(\d+)\s+(\d{1,2}/\d{1,2}/\d{2,4})\s+(.+)$', line.strip())
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
                'total_entries': len(entries)
            }
            
            print(json.dumps(result, indent=2))
            
        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
            print(json.dumps(result, indent=2))
        
        finally:
            await browser.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python playwright_scrape_cl.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    asyncio.run(scrape_docket_playwright(url))
