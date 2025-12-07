import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time

def scrape_website(url):
    """
    Advanced web scraper with multiple fallback strategies
    """
    # Try multiple scraping strategies
    strategies = [
        scrape_with_session,
        scrape_with_basic_headers,
        scrape_with_minimal_request
    ]
    
    for strategy in strategies:
        try:
            result = strategy(url)
            if result['success']:
                return result
        except:
            continue
    
    # If all strategies fail, return error
    return {
        'success': False,
        'error': 'Unable to access website. It may have anti-scraping protection. Try a different URL or the company blog/documentation page.',
        'url': url
    }

def scrape_with_session(url):
    """Strategy 1: Full browser simulation with session"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    # Add small delay to appear more human
    time.sleep(0.5)
    
    response = session.get(url, timeout=20, allow_redirects=True, verify=True)
    response.raise_for_status()
    
    return process_response(response, url)

def scrape_with_basic_headers(url):
    """Strategy 2: Simple headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
    response.raise_for_status()
    
    return process_response(response, url)

def scrape_with_minimal_request(url):
    """Strategy 3: Minimal request"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    return process_response(response, url)

def process_response(response, url):
    """Process the HTTP response and extract data"""
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup(["script", "style", "noscript", "iframe", "svg"]):
        element.decompose()
    
    # Extract data
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
    
    # Validate we got meaningful data
    total_content = len(scraped_data['headings']) + len(scraped_data['paragraphs']) + len(scraped_data['lists'])
    
    if total_content < 3:
        return {
            'success': False,
            'error': 'Website returned minimal content. It may be JavaScript-heavy or blocking scrapers.',
            'url': url
        }
    
    return {
        'success': True,
        'data': scraped_data,
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
            if text and len(text) > 2 and len(text) < 200:
                headings.append(text)
    return headings[:50]  # Limit to 50 headings

def extract_all_paragraphs(soup):
    """Extract ALL paragraphs"""
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text and len(text) > 20:
            paragraphs.append(text)
    return paragraphs[:100]  # Limit to 100 paragraphs

def extract_all_lists(soup):
    """Extract content from all lists"""
    list_items = []
    for list_tag in soup.find_all(['ul', 'ol']):
        for li in list_tag.find_all('li', recursive=False):
            text = li.get_text().strip()
            if text and 5 < len(text) < 300:
                list_items.append(text)
    return list_items[:100]  # Limit to 100 items

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
    
    for section in soup.find_all(['section', 'article', 'div', 'main']):
        section_id = section.get('id', '')
        section_class = ' '.join(section.get('class', []))
        
        if not section_id and not section_class:
            continue
            
        key = section_id or section_class
        if len(key) > 100:
            continue
            
        text = section.get_text().strip()
        if text and 50 < len(text) < 5000:
            sections[key] = text
    
    return dict(list(sections.items())[:20])  # Limit to 20 sections

def extract_full_text(soup):
    """Extract all visible text"""
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text[:25000]  # 25000 characters

def format_scraped_data_for_ai(scraped_data):
    """Format scraped data into RICH context for AI"""
    if not scraped_data or 'data' not in scraped_data:
        return ""
    
    data = scraped_data['data']
    sections = []
    
    # Title and Description
    sections.append(f"COMPANY: {data.get('title', 'N/A')}")
    if data.get('meta_description'):
        sections.append(f"\nDESCRIPTION: {data['meta_description']}")
    
    # Headings
    headings = data.get('headings', [])
    if headings:
        sections.append(f"\n\nKEY TOPICS:")
        for h in headings[:25]:
            sections.append(f"• {h}")
    
    # Lists (Services/Features)
    lists = data.get('lists', [])
    if lists:
        sections.append(f"\n\nSERVICES & FEATURES:")
        for item in lists[:40]:
            sections.append(f"• {item}")
    
    # Contact Info
    contact = data.get('contact_info', {})
    if contact.get('emails') or contact.get('phones'):
        sections.append("\n\nCONTACT INFORMATION:")
        if contact.get('emails'):
            sections.append(f"📧 Emails: {', '.join(contact['emails'][:3])}")
        if contact.get('phones'):
            sections.append(f"📞 Phones: {', '.join(contact['phones'][:3])}")
    
    # Paragraphs (Detailed Content)
    paragraphs = data.get('paragraphs', [])
    if paragraphs:
        sections.append(f"\n\nDETAILED CONTENT:")
        for p in paragraphs[:50]:
            if len(p) > 30:
                sections.append(f"\n{p}")
    
    # Sections
    section_data = data.get('sections', {})
    if section_data:
        sections.append("\n\nADDITIONAL INFORMATION:")
        for key, value in list(section_data.items())[:15]:
            if len(value) > 100:
                sections.append(f"\n[{key[:50]}]:\n{value[:800]}")
    
    return '\n'.join(sections)
