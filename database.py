import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Database connection pool for better performance
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "chatbot_db"),
    "pool_name": "chatbot_pool",
    "pool_size": 5
}

try:
    connection_pool = pooling.MySQLConnectionPool(**db_config)
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    connection_pool = None

def get_connection():
    """Get a connection from the pool"""
    if connection_pool:
        return connection_pool.get_connection()
    return None

def create_tables():
    """Create necessary database tables if they don't exist"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Companies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                website_url VARCHAR(500) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_company_name (company_name)
            )
        """)
        
        # Scraped data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_id INT NOT NULL,
                content_type VARCHAR(50),
                content_text TEXT,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
                INDEX idx_company_id (company_id)
            )
        """)
        
        # Chat history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_id INT NOT NULL,
                user_question TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                response_time_ms INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
                INDEX idx_company_id_created (company_id, created_at)
            )
        """)
        
        conn.commit()
        print("Database tables created successfully!")
        return True
        
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def save_company(company_name, website_url):
    """Save or update company information"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    
    try:
        # Check if company already exists
        cursor.execute(
            "SELECT id FROM companies WHERE company_name = %s AND website_url = %s",
            (company_name, website_url)
        )
        result = cursor.fetchone()
        
        if result:
            company_id = result[0]
            # Update timestamp
            cursor.execute(
                "UPDATE companies SET updated_at = NOW() WHERE id = %s",
                (company_id,)
            )
        else:
            # Insert new company
            cursor.execute(
                "INSERT INTO companies (company_name, website_url) VALUES (%s, %s)",
                (company_name, website_url)
            )
            company_id = cursor.lastrowid
        
        conn.commit()
        return company_id
        
    except mysql.connector.Error as err:
        print(f"Error saving company: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def save_scraped_data(company_id, content_type, content_text, metadata=None):
    """Save scraped website data"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO scraped_data (company_id, content_type, content_text, metadata) VALUES (%s, %s, %s, %s)",
            (company_id, content_type, content_text, str(metadata) if metadata else None)
        )
        conn.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Error saving scraped data: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_company_data(company_id):
    """Retrieve all scraped data for a company"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get company info
        cursor.execute(
            "SELECT * FROM companies WHERE id = %s",
            (company_id,)
        )
        company = cursor.fetchone()
        
        if not company:
            return None
        
        # Get scraped data
        cursor.execute(
            "SELECT content_type, content_text FROM scraped_data WHERE company_id = %s",
            (company_id,)
        )
        scraped_data = cursor.fetchall()
        
        return {
            "company": company,
            "scraped_data": scraped_data
        }
        
    except mysql.connector.Error as err:
        print(f"Error retrieving company data: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def save_chat_history(company_id, user_question, bot_response, response_time_ms):
    """Save chat interaction to history"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO chat_history (company_id, user_question, bot_response, response_time_ms) VALUES (%s, %s, %s, %s)",
            (company_id, user_question, bot_response, response_time_ms)
        )
        conn.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Error saving chat history: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_latest_company():
    """Get the most recently created/updated company"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            "SELECT * FROM companies ORDER BY updated_at DESC LIMIT 1"
        )
        return cursor.fetchone()
        
    except mysql.connector.Error as err:
        print(f"Error getting latest company: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def clear_company_data(company_id):
    """Clear all scraped data for a company (for re-scraping)"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "DELETE FROM scraped_data WHERE company_id = %s",
            (company_id,)
        )
        conn.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"Error clearing company data: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
