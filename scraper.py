import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def scrape_website(url):
    """
    Enhanced web scraper with anti-bot bypass
    """
    try:
        # Enhanced headers to bypass 403 Forbidden
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
        }
        
        # Add session for better compatibility
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
        
        # Extract EVERYTHING
        scraped_data = {
            'title': extract_title(soup),
            'meta_description': extract_meta_description(soup),
            'headings': extract_all_headings(soup),
            'paragraphs': extract_all_paragraphs(soup),
            'lists': extract_all_lists(soup),
            'contact_info': extract_contact_info(soup, response.text),
            'sections': extract_all_sections(soup),
            'full_text': extract_full_text(soup)
        }
        
        return {
            'success': True,
            'data': scraped_data,
            'url': url
        }
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            return {
                'success': False,
                'error': f'Website blocked access (403 Forbidden). Try a different URL or the website may have anti-scraping protection.',
                'url': url
            }
        return {
            'success': False,
            'error': f'HTTP Error {e.response.status_code}: {str(e)}',
            'url': url
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error: {str(e)}',
            'url': url
        }

def extract_title(soup):
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text().strip()
    return "Company Website"

def extract_meta_description(soup):
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        return meta_desc['content'].strip()
    meta_desc = soup.find('meta', attrs={'property': 'og:description'})
    if meta_desc and meta_desc.get('content'):
        return meta_desc['content'].strip()
    return ""

def extract_all_headings(soup):
    """Extract ALL headings"""
    headings = []
    for i in range(1, 7):
        for heading in soup.find_all(f'h{i}'):
            text = heading.get_text().strip()
            if text and len(text) > 2:
                headings.append(text)
    return headings

def extract_all_paragraphs(soup):
    """Extract ALL paragraphs"""
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text and len(text) > 15:
            paragraphs.append(text)
    return paragraphs

def extract_all_lists(soup):
    """Extract content from all lists"""
    list_items = []
    for list_tag in soup.find_all(['ul', 'ol']):
        for li in list_tag.find_all('li', recursive=False):
            text = li.get_text().strip()
            if text and len(text) > 5:
                list_items.append(text)
    return list_items

def extract_contact_info(soup, html_text):
    """Extract contact information"""
    contact_info = {
        'emails': [],
        'phones': []
    }
    
    # Extract emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, html_text)
    contact_info['emails'] = list(set(emails))[:5]
    
    # Extract phone numbers
    phone_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    phones = re.findall(phone_pattern, html_text)
    contact_info['phones'] = list(set(phones))[:5]
    
    return contact_info

def extract_all_sections(soup):
    """Extract content organized by sections"""
    sections = {}
    
    for section in soup.find_all(['section', 'article', 'div']):
        section_id = section.get('id', '')
        section_class = ' '.join(section.get('class', []))
        
        if not section_id and not section_class:
            continue
            
        key = section_id or section_class
        if len(key) > 100:
            continue
            
        text = section.get_text().strip()
        if text and 30 < len(text) < 3000:
            sections[key] = text
    
    return sections

def extract_full_text(soup):
    """Extract all visible text"""
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text[:20000]

def format_scraped_data_for_ai(scraped_data):
    """Format scraped data into RICH context for AI"""
    if not scraped_data or 'data' not in scraped_data:
        return ""
    
    data = scraped_data['data']
    sections = []
    
    sections.append(f"COMPANY: {data.get('title', 'N/A')}")
    sections.append(f"\nDESCRIPTION: {data.get('meta_description', 'N/A')}")
    
    headings = data.get('headings', [])
    if headings:
        sections.append(f"\n\nKEY SECTIONS:")
        for h in headings[:20]:
            sections.append(f"- {h}")
    
    lists = data.get('lists', [])
    if lists:
        sections.append(f"\n\nSERVICES/FEATURES:")
        for item in lists[:30]:
            sections.append(f"- {item}")
    
    contact = data.get('contact_info', {})
    if contact.get('emails') or contact.get('phones'):
        sections.append("\n\nCONTACT:")
        if contact.get('emails'):
            sections.append(f"Emails: {', '.join(contact['emails'][:3])}")
        if contact.get('phones'):
            sections.append(f"Phones: {', '.join(contact['phones'][:3])}")
    
    paragraphs = data.get('paragraphs', [])
    if paragraphs:
        sections.append(f"\n\nDETAILED INFORMATION:")
        for p in paragraphs[:40]:
            sections.append(p)
    
    section_data = data.get('sections', {})
    if section_data:
        sections.append("\n\nORGANIZED CONTENT:")
        for key, value in list(section_data.items())[:10]:
            sections.append(f"\n[{key}]:\n{value[:500]}")
    
    return '\n'.join(sections)
