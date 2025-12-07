import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import re

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-001')
else:
    model = None

# Response cache
response_cache = {}

def generate_response(user_question, company_context, company_name):
    """Generate intelligent AI response with smart fallback"""
    start_time = time.time()
    
    # Try Gemini API first
    if model:
        try:
            cache_key = f"{company_name}:{user_question.lower().strip()}"
            if cache_key in response_cache:
                response_time = int((time.time() - start_time) * 1000)
                return {
                    'success': True,
                    'response': response_cache[cache_key],
                    'response_time_ms': response_time,
                    'cached': True
                }
            
            # Build prompt
            prompt = f"""You are a helpful AI assistant for {company_name}. Answer the user's question based ONLY on the provided information. Be conversational, natural, and specific. Give different answers for different questions.

Company Information:
{company_context}

User Question: {user_question}

Provide a helpful, natural response (2-4 sentences):"""
            
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            response = model.generate_content(
                prompt,
                generation_config={'temperature': 0.8, 'max_output_tokens': 500},
                safety_settings=safety_settings
            )
            
            if response and hasattr(response, 'text') and response.text:
                response_text = response.text.strip()
                response_cache[cache_key] = response_text
                response_time = int((time.time() - start_time) * 1000)
                
                return {
                    'success': True,
                    'response': response_text,
                    'response_time_ms': response_time,
                    'cached': False
                }
                
        except Exception as e:
            error_msg = str(e)
            if '429' not in error_msg and 'quota' not in error_msg.lower():
                # Not a quota error, return error
                response_time = int((time.time() - start_time) * 1000)
                return {
                    'success': False,
                    'error': f'AI Error: {error_msg}',
                    'response_time_ms': response_time
                }
    
    # Use intelligent fallback
    response_time = int((time.time() - start_time) * 1000)
    fallback_response = generate_intelligent_fallback(user_question, company_context, company_name)
    
    cache_key = f"{company_name}:{user_question.lower().strip()}"
    response_cache[cache_key] = fallback_response
    
    return {
        'success': True,
        'response': fallback_response,
        'response_time_ms': response_time,
        'fallback': True
    }

def generate_intelligent_fallback(user_question, company_context, company_name):
    """Smart fallback that gives contextual, varied responses"""
    question_lower = user_question.lower().strip()
    
    # Parse context into structured data
    data = parse_context(company_context)
    
    # Detect question intent
    intent = detect_intent(question_lower)
    
    # Generate contextual response based on intent
    if intent == 'services':
        return generate_services_answer(data, company_name, question_lower)
    elif intent == 'about':
        return generate_about_answer(data, company_name, question_lower)
    elif intent == 'contact':
        return generate_contact_answer(data, company_name)
    elif intent == 'location':
        return generate_location_answer(data, company_name)
    elif intent == 'specific':
        return generate_specific_answer(data, company_name, question_lower)
    else:
        return generate_general_answer(data, company_name, question_lower)

def parse_context(context):
    """Parse context into structured data"""
    data = {
        'title': '',
        'description': '',
        'headings': [],
        'services': [],
        'paragraphs': [],
        'emails': [],
        'phones': []
    }
    
    lines = context.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('COMPANY:'):
            data['title'] = line.replace('COMPANY:', '').strip()
        elif line.startswith('DESCRIPTION:'):
            data['description'] = line.replace('DESCRIPTION:', '').strip()
        elif 'KEY TOPICS:' in line:
            current_section = 'headings'
        elif 'SERVICES & FEATURES:' in line:
            current_section = 'services'
        elif 'DETAILED CONTENT:' in line:
            current_section = 'paragraphs'
        elif 'CONTACT' in line:
            current_section = 'contact'
        elif current_section == 'headings' and line.startswith('•'):
            data['headings'].append(line[1:].strip())
        elif current_section == 'services' and line.startswith('•'):
            data['services'].append(line[1:].strip())
        elif current_section == 'paragraphs' and len(line) > 30:
            data['paragraphs'].append(line)
        elif current_section == 'contact':
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', line)
            data['emails'].extend(emails)
    
    return data

def detect_intent(question):
    """Detect what the user is asking about"""
    if any(word in question for word in ['service', 'offer', 'provide', 'do', 'solution', 'product']):
        return 'services'
    elif any(word in question for word in ['about', 'who', 'what is', 'overview', 'company', 'business']):
        return 'about'
    elif any(word in question for word in ['contact', 'email', 'phone', 'reach', 'call']):
        return 'contact'
    elif any(word in question for word in ['where', 'location', 'located', 'address', 'office']):
        return 'location'
    elif any(word in question for word in ['ai', 'erp', 'zoho', 'hubspot', 'web', 'mobile', 'digital']):
        return 'specific'
    else:
        return 'general'

def generate_services_answer(data, company_name, question):
    """Generate answer about services"""
    if data['services']:
        # Pick relevant services based on question
        if 'ai' in question:
            relevant = [s for s in data['services'] if 'ai' in s.lower() or 'artificial' in s.lower()]
        elif 'web' in question or 'website' in question:
            relevant = [s for s in data['services'] if 'web' in s.lower() or 'website' in s.lower()]
        elif 'mobile' in question or 'app' in question:
            relevant = [s for s in data['services'] if 'mobile' in s.lower() or 'app' in s.lower()]
        else:
            relevant = data['services'][:6]
        
        if relevant:
            return f"{company_name} offers several key services:\n\n" + '\n'.join([f"• {s}" for s in relevant[:5]])
        else:
            return f"{company_name} provides:\n\n" + '\n'.join([f"• {s}" for s in data['services'][:6]])
    elif data['description']:
        return f"{company_name} is {data['description']}"
    else:
        return f"{company_name} offers various technology and business solutions. Visit their website for detailed service information."

def generate_about_answer(data, company_name, question):
    """Generate answer about the company"""
    response_parts = []
    
    if data['description']:
        response_parts.append(data['description'])
    
    if data['paragraphs']:
        # Find most relevant paragraph
        for para in data['paragraphs'][:3]:
            if any(word in para.lower() for word in ['company', 'business', 'founded', 'mission', 'vision']):
                response_parts.append(f"\n{para}")
                break
    
    if not response_parts and data['services']:
        response_parts.append(f"{company_name} specializes in: {', '.join(data['services'][:4])}")
    
    return '\n'.join(response_parts) if response_parts else f"{company_name} is a technology company. For more details, please visit their website."

def generate_contact_answer(data, company_name):
    """Generate answer about contact information"""
    if data['emails'] or data['phones']:
        response = f"You can contact {company_name}:\n\n"
        if data['emails']:
            response += f"📧 Email: {data['emails'][0]}\n"
        if data['phones']:
            response += f"📞 Phone: {data['phones'][0]}"
        return response
    else:
        return f"Contact information for {company_name} can be found on their website. Please visit their contact page for email and phone details."

def generate_location_answer(data, company_name):
    """Generate answer about location"""
    # Search for location in description and paragraphs
    location_keywords = ['singapore', 'india', 'usa', 'uk', 'location', 'based', 'office']
    
    if data['description']:
        for keyword in location_keywords:
            if keyword in data['description'].lower():
                return f"Based on the information available: {data['description']}"
    
    for para in data['paragraphs'][:5]:
        for keyword in location_keywords:
            if keyword in para.lower():
                return para
    
    if 'singapore' in data['title'].lower() or 'singapore' in data['description'].lower():
        return f"{company_name} is based in Singapore, serving global enterprises with IT solutions."
    
    return f"Location information for {company_name} can be found on their website's contact or about page."

def generate_specific_answer(data, company_name, question):
    """Generate answer for specific service questions"""
    # Extract the specific service being asked about
    keywords = question.split()
    
    # Search in services and paragraphs
    relevant = []
    for service in data['services']:
        if any(keyword in service.lower() for keyword in keywords if len(keyword) > 3):
            relevant.append(service)
    
    if relevant:
        return f"Regarding your question about {company_name}:\n\n" + '\n'.join([f"• {s}" for s in relevant[:4]])
    
    # Search in paragraphs
    for para in data['paragraphs']:
        if any(keyword in para.lower() for keyword in keywords if len(keyword) > 3):
            return para
    
    return generate_services_answer(data, company_name, question)

def generate_general_answer(data, company_name, question):
    """Generate general answer by searching content"""
    keywords = [word for word in question.split() if len(word) > 3]
    
    # Search paragraphs
    for para in data['paragraphs']:
        if any(keyword in para.lower() for keyword in keywords):
            return para
    
    # Search services
    relevant_services = []
    for service in data['services']:
        if any(keyword in service.lower() for keyword in keywords):
            relevant_services.append(service)
    
    if relevant_services:
        return f"{company_name}:\n\n" + '\n'.join([f"• {s}" for s in relevant_services[:5]])
    
    # Default to description
    if data['description']:
        return data['description']
    
    return f"For detailed information about {company_name}, please visit their website."

def test_ai_connection():
    """Test AI API"""
    try:
        if not GEMINI_API_KEY or not model:
            return {'success': False, 'error': 'API key not configured'}
        
        response = model.generate_content("Say 'AI is working'")
        
        if response and response.text:
            return {'success': True, 'message': 'AI connection successful'}
        else:
            return {'success': False, 'error': 'No response generated'}
            
    except Exception as e:
        if '429' in str(e) or 'quota' in str(e).lower():
            return {'success': False, 'error': 'API quota exceeded. Using intelligent fallback.', 'fallback_available': True}
        return {'success': False, 'error': f'AI error: {str(e)}'}
