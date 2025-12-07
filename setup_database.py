import mysql.connector
import os

print("Setting up enhanced database with user authentication...")

# Connect without database first
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Hirthick#6'
    )
    cursor = conn.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot_db")
    print("✓ Database 'chatbot_db' created!")
    
    conn.close()
    
    # Now connect to the database and create tables
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Hirthick#6',
        database='chatbot_db'
    )
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            is_active BOOLEAN DEFAULT TRUE,
            INDEX idx_username (username),
            INDEX idx_email (email)
        )
    """)
    print("✓ Users table created!")
    
    # Create companies table (with user_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            company_name VARCHAR(255) NOT NULL,
            website_url VARCHAR(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_company_name (company_name)
        )
    """)
    print("✓ Companies table created!")
    
    # Create scraped_data table
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
    print("✓ Scraped data table created!")
    
    # Create chat_history table (with user_id)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT DEFAULT 1,
            company_id INT NOT NULL,
            user_question TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            response_time_ms INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
            INDEX idx_company_id_created (company_id, created_at)
        )
    """)
    print("✓ Chat history table created!")
    
    # Create user_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            session_token VARCHAR(255) NOT NULL UNIQUE,
            ip_address VARCHAR(45),
            user_agent TEXT,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_session_token (session_token),
            INDEX idx_user_id (user_id)
        )
    """)
    print("✓ User sessions table created!")
    
    # Insert default demo user
    cursor.execute("""
        INSERT IGNORE INTO users (username, email, password_hash, is_active) 
        VALUES ('demo', 'demo@example.com', 'demo123', TRUE)
    """)
    print("✓ Default demo user created (username: demo, password: demo123)!")
    
    conn.commit()
    print("\n✅ Enhanced database setup complete with user authentication!")
    print("\nNew Tables:")
    print("  - users (username, email, password_hash, timestamps)")
    print("  - companies (linked to users)")
    print("  - scraped_data")
    print("  - chat_history (linked to users)")
    print("  - user_sessions")
    print("\nYou can now run: python app.py")
    
    conn.close()
    
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
    print("\nMake sure MySQL is running and password is correct!")
