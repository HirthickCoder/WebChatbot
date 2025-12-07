from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import time

# Import our modules
import database
import scraper
import ai_chatbot

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for frontend

# Global variable to store current chatbot context
current_chatbot = {
    'company_id': None,
    'company_name': None,
    'website_url': None,
    'context': None,
    'ready': False
}

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'AI Chatbot Assistant API is running',
        'endpoints': {
            'create_chatbot': '/create-chatbot [POST]',
            'chat': '/chat [POST]',
            'status': '/chatbot-status [GET]',
            'test_ai': '/test-ai [GET]'
        }
    })

@app.route('/create-chatbot', methods=['POST'])
def create_chatbot():
    """
    Create a new chatbot by scraping website
    Expected JSON: { "company_name": "...", "website_url": "..." }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        company_name = data.get('company_name', '').strip()
        website_url = data.get('website_url', '').strip()
        
        if not company_name or not website_url:
            return jsonify({
                'success': False,
                'error': 'Both company_name and website_url are required'
            }), 400
        
        # Ensure URL has protocol
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        print(f"Creating chatbot for {company_name} - {website_url}")
        
        # Scrape website
        print("Scraping website...")
        scraped_result = scraper.scrape_website(website_url)
        
        if not scraped_result['success']:
            return jsonify({
                'success': False,
                'error': scraped_result.get('error', 'Failed to scrape website')
            }), 500
        
        
        # Save to database (optional - works without database)
        company_id = None
        try:
            print("Saving to database...")
            company_id = database.save_company(company_name, website_url)
            
            if company_id:
                # Clear old scraped data for this company
                database.clear_company_data(company_id)
                
                # Save scraped data
                scraped_data = scraped_result['data']
                database.save_scraped_data(company_id, 'title', scraped_data.get('title', ''))
                database.save_scraped_data(company_id, 'meta_description', scraped_data.get('meta_description', ''))
                database.save_scraped_data(company_id, 'full_text', scraped_data.get('full_text', ''))
                database.save_scraped_data(company_id, 'contact_info', str(scraped_data.get('contact_info', {})))
                database.save_scraped_data(company_id, 'services', ', '.join(scraped_data.get('services', [])))
                print(f"Data saved to database! Company ID: {company_id}")
        except Exception as db_error:
            print(f"Database not available (this is OK): {str(db_error)}")
            company_id = 1  # Use dummy ID for in-memory operation
        
        # Format context for AI
        context = scraper.format_scraped_data_for_ai(scraped_result)
        
        # Update global chatbot state
        current_chatbot['company_id'] = company_id
        current_chatbot['company_name'] = company_name
        current_chatbot['website_url'] = website_url
        current_chatbot['context'] = context
        current_chatbot['ready'] = True
        
        print(f"Chatbot created successfully!")
        
        return jsonify({
            'success': True,
            'message': f'Chatbot created for {company_name}',
            'company_id': company_id,
            'data_extracted': {
                'title': scraped_result['data'].get('title', ''),
                'services_count': len(scraped_result['data'].get('services', [])),
                'has_contact_info': bool(scraped_result['data'].get('contact_info', {}).get('emails'))
            }
        })
        
    except Exception as e:
        print(f"Error in create_chatbot: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Answer user questions about the company
    Expected JSON: { "question": "..." }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question is required'
            }), 400
        
        # Check if chatbot is ready
        if not current_chatbot['ready']:
            return jsonify({
                'success': False,
                'error': 'Please create a chatbot first by providing a company URL'
            }), 400
        
        print(f"Processing question: {question}")
        start_time = time.time()
        
        # Generate AI response
        ai_result = ai_chatbot.generate_response(
            question,
            current_chatbot['context'],
            current_chatbot['company_name']
        )
        
        if not ai_result['success']:
            return jsonify({
                'success': False,
                'error': ai_result.get('error', 'Failed to generate response')
            }), 500
        
        response_text = ai_result['response']
        response_time_ms = ai_result['response_time_ms']
        
        # Save to chat history (optional)
        try:
            database.save_chat_history(
                current_chatbot['company_id'],
                question,
                response_text,
                response_time_ms
            )
        except Exception as db_error:
            print(f"Could not save chat history (database not available): {str(db_error)}")
        
        print(f"Response generated in {response_time_ms}ms")
        
        return jsonify({
            'success': True,
            'response': response_text,
            'response_time_ms': response_time_ms,
            'cached': ai_result.get('cached', False)
        })
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/chatbot-status', methods=['GET'])
def chatbot_status():
    """Get current chatbot status"""
    return jsonify({
        'ready': current_chatbot['ready'],
        'company_name': current_chatbot.get('company_name'),
        'website_url': current_chatbot.get('website_url'),
        'company_id': current_chatbot.get('company_id')
    })

@app.route('/test-ai', methods=['GET'])
def test_ai():
    """Test AI connection"""
    result = ai_chatbot.test_ai_connection()
    return jsonify(result)

@app.route('/test-db', methods=['GET'])
def test_db():
    """Test database connection"""
    try:
        conn = database.get_connection()
        if conn:
            conn.close()
            return jsonify({
                'success': True,
                'message': 'Database connection successful'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to connect to database'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Initialize database tables (optional)
    try:
        print("Initializing database...")
        database.create_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Database not available (running without database): {str(e)}")
    
    # Start Flask server
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
