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

# Use Gemini 2.0 Flash for fast responses
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Response cache for common questions
response_cache = {}

def generate_response(user_question, company_context, company_name):
    """Generate AI response with fallback"""
    start_time = time.time()
    
    try:
        # Check cache first
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
        prompt = f"""You are a helpful AI assistant for {company_name}. Answer based ONLY on the provided information. Be concise (2-4 sentences).

Company Information:
{company_context}

User Question: {user_question}

Answer:"""
        
        # Generate response
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        response = model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 500},
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
        response_time = int((time.time() - start_time) * 1000)
        error_msg = str(e)
        
        # Use fallback for quota errors
        if '429' in error_msg or 'quota' in error_msg.lower():
            fallback_response = generate_fallback_response(user_question, company_context, company_name)
            response_cache[cache_key] = fallback_response
            
            return {
                'success': True,
                'response': fallback_response,
                'response_time_ms': response_time,
                'fallback': True
            }
        
        return {
            'success': False,
            'error': f'AI Error: {error_msg}',
            'response_time_ms': response_time
        }

def generate_fallback_response(user_question, company_context, company_name):
    """Simple fallback using scraped data"""
    question_lower = user_question.lower()
    
    # Search for relevant content
    lines = company_context.split('\n')
    relevant = []
    
    # Extract keywords
    keywords = [w for w in question_lower.split() if len(w) > 3]
    
    # Find relevant lines
    for line in lines:
        if any(keyword in line.lower() for keyword in keywords):
            if len(line.strip()) > 20:
                relevant.append(line.strip())
                if len(relevant) >= 5:
                    break
    
    if relevant:
        return f"{company_name}:\n\n" + '\n\n'.join(relevant[:3])
    
    # Default response
    if 'service' in question_lower or 'do' in question_lower:
        for line in lines:
            if 'SERVICES' in line or 'FEATURES' in line:
                idx = lines.index(line)
                services = [lines[i].strip() for i in range(idx+1, min(idx+10, len(lines))) if lines[i].strip().startswith('-')]
                if services:
                    return f"{company_name} offers:\n" + '\n'.join(services[:8])
    
    if 'contact' in question_lower:
        for line in lines:
            if 'Email' in line or 'Phone' in line:
                return line
    
    # Return first few meaningful lines
    meaningful = [l.strip() for l in lines if len(l.strip()) > 30]
    if meaningful:
        return '\n\n'.join(meaningful[:3])
    
    return f"{company_name} - For more information, please visit their website."

def test_ai_connection():
    """Test AI API"""
    try:
        if not GEMINI_API_KEY:
            return {'success': False, 'error': 'API key not configured'}
        
        response = model.generate_content("Say 'AI is working'")
        
        if response and response.text:
            return {'success': True, 'message': 'AI connection successful'}
        else:
            return {'success': False, 'error': 'No response generated'}
            
    except Exception as e:
        if '429' in str(e) or 'quota' in str(e).lower():
            return {'success': False, 'error': 'API quota exceeded. Using fallback.', 'fallback_available': True}
        return {'success': False, 'error': f'AI error: {str(e)}'}
