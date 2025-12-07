# AI Chatbot Assistant 🤖

A powerful AI-powered chatbot that extracts company information from websites and answers questions instantly (< 3 seconds response time). Built with Flask, MySQL, and Google Gemini AI.

![Chatbot Interface](https://img.shields.io/badge/Status-Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)

## ✨ Features

- 🌐 **Web Scraping**: Automatically extracts company information from any website
- 💬 **AI-Powered Chat**: Instant responses using Google Gemini AI
- 🗄️ **MySQL Database**: Stores company data and chat history
- ⚡ **Fast Response**: < 3 second response time with caching
- 🎨 **Beautiful UI**: Modern dark theme with glassmorphism effects
- 📱 **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Google Gemini API key (free)

### Installation

1. **Clone or navigate to the project folder:**
   ```bash
   cd c:\Users\Hirthick\Videos\SYN
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database:**
   - Follow the detailed guide: [MYSQL_SETUP_GUIDE.md](MYSQL_SETUP_GUIDE.md)
   - Or quick setup:
     ```bash
     mysql -u root -p
     CREATE DATABASE chatbot_db;
     USE chatbot_db;
     SOURCE database_schema.sql;
     ```

4. **Configure environment variables:**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` file:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=chatbot_db
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Get your Gemini API key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in and create a free API key
   - Add it to your `.env` file

### Running the Application

1. **Start the Flask backend:**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   Initializing database...
   Database tables created successfully!
   Starting Flask server...
   * Running on http://0.0.0.0:5000
   ```

2. **Open the frontend:**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     python -m http.server 8000
     ```
   - Then visit: http://localhost:8000

## 📖 How to Use

1. **Create a Chatbot:**
   - Enter a company name (e.g., "Google")
   - Enter the website URL (e.g., "https://www.google.com")
   - Click "Create Chatbot"
   - Wait for the success message

2. **Ask Questions:**
   - Type your question in the chat input
   - Press Enter or click "Send"
   - Get instant AI-powered responses!

### Example Questions:
- "What does this company do?"
- "What services do they offer?"
- "How can I contact them?"
- "Tell me about the company"

## 🏗️ Project Structure

```
SYN/
├── app.py                  # Main Flask application
├── database.py             # MySQL database operations
├── scraper.py              # Web scraping module
├── ai_chatbot.py           # AI chatbot logic (Gemini)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── database_schema.sql     # MySQL database schema
├── index.html              # Frontend HTML
├── style.css               # Frontend styling
├── script.js               # Frontend JavaScript
├── README.md               # This file
└── MYSQL_SETUP_GUIDE.md    # MySQL setup instructions
```

## 🔌 API Endpoints

### Health Check
```
GET /
```
Returns API status and available endpoints.

### Create Chatbot
```
POST /create-chatbot
Content-Type: application/json

{
  "company_name": "Google",
  "website_url": "https://www.google.com"
}
```

### Chat
```
POST /chat
Content-Type: application/json

{
  "question": "What does this company do?"
}
```

### Get Chatbot Status
```
GET /chatbot-status
```

### Test Database Connection
```
GET /test-db
```

### Test AI Connection
```
GET /test-ai
```

## 🛠️ Technologies Used

### Backend
- **Flask**: Web framework
- **BeautifulSoup4**: Web scraping
- **MySQL**: Database
- **Google Gemini AI**: AI responses
- **Python-dotenv**: Environment configuration

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with glassmorphism
- **JavaScript**: Interactivity
- **Fetch API**: Backend communication

## ⚙️ Configuration

### Database Configuration
Edit `.env` file:
```
DB_HOST=localhost          # MySQL host
DB_USER=root               # MySQL username
DB_PASSWORD=your_password  # MySQL password
DB_NAME=chatbot_db         # Database name
```

### AI Configuration
```
GEMINI_API_KEY=your_key    # Get from Google AI Studio
```

### Flask Configuration
```
FLASK_ENV=development      # development or production
FLASK_DEBUG=True           # Enable debug mode
```

## 🐛 Troubleshooting

### "Failed to connect to database"
- Make sure MySQL is running
- Check your credentials in `.env`
- Run: `python app.py` and check for errors

### "AI Error: API key not configured"
- Get your Gemini API key from https://makersuite.google.com/app/apikey
- Add it to `.env` file
- Restart the Flask server

### "Failed to scrape website"
- Check if the URL is accessible
- Some websites block scrapers
- Try adding `https://` to the URL

### "No response from server"
- Make sure Flask is running on port 5000
- Check if `API_BASE_URL` in `script.js` is correct
- Open browser console (F12) for errors

## 📊 Database Schema

### Companies Table
- `id`: Primary key
- `company_name`: Company name
- `website_url`: Website URL
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Scraped Data Table
- `id`: Primary key
- `company_id`: Foreign key to companies
- `content_type`: Type of content (title, description, etc.)
- `content_text`: Extracted content
- `metadata`: Additional metadata (JSON)
- `created_at`: Creation timestamp

### Chat History Table
- `id`: Primary key
- `company_id`: Foreign key to companies
- `user_question`: User's question
- `bot_response`: AI's response
- `response_time_ms`: Response time in milliseconds
- `created_at`: Creation timestamp

## 🚀 Performance Optimization

- **Response Caching**: Common questions are cached for instant responses
- **Connection Pooling**: MySQL connection pool for better performance
- **Gemini Flash Model**: Using fast Gemini 1.5 Flash for < 3s responses
- **Content Limiting**: Scraped content is limited to optimize AI context

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use strong MySQL passwords
- Keep your Gemini API key secret
- Consider rate limiting for production use
- Validate and sanitize user inputs

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📧 Support

If you encounter any issues:
1. Check the [MYSQL_SETUP_GUIDE.md](MYSQL_SETUP_GUIDE.md)
2. Review the troubleshooting section above
3. Check the browser console for errors
4. Verify Flask server logs

## 🎯 Next Steps

- [ ] Add user authentication
- [ ] Support multiple chatbots simultaneously
- [ ] Add export chat history feature
- [ ] Implement voice input/output
- [ ] Add analytics dashboard
- [ ] Deploy to cloud (AWS, Azure, or Heroku)

---

**Built with ❤️ using Flask, MySQL, and Google Gemini AI**
