-- Enhanced AI Chatbot Assistant Database Schema with User Authentication
-- MySQL Database Setup

-- Create database
CREATE DATABASE IF NOT EXISTS chatbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE chatbot_db;

-- Users table: Store user authentication information
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Companies table: Store company information (linked to users)
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    website_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_company_name (company_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Scraped data table: Store extracted website content
CREATE TABLE IF NOT EXISTS scraped_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    content_type VARCHAR(50) COMMENT 'Type of content: title, meta_description, full_text, etc.',
    content_text TEXT,
    metadata JSON COMMENT 'Additional metadata in JSON format',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    INDEX idx_company_id (company_id),
    INDEX idx_content_type (content_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chat history table: Store user questions and bot responses
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company_id INT NOT NULL,
    user_question TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    response_time_ms INT COMMENT 'Response time in milliseconds',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    INDEX idx_user_company (user_id, company_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User sessions table: Track active user sessions
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_token (session_token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- API usage tracking: Monitor API calls and quota
CREATE TABLE IF NOT EXISTS api_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    api_name VARCHAR(50) COMMENT 'gemini, openai, etc.',
    request_count INT DEFAULT 0,
    tokens_used INT DEFAULT 0,
    last_request_at TIMESTAMP NULL,
    quota_reset_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_api (user_id, api_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional: Create a view for easy querying
CREATE OR REPLACE VIEW user_activity AS
SELECT 
    u.id as user_id,
    u.username,
    u.email,
    COUNT(DISTINCT c.id) as total_companies,
    COUNT(DISTINCT ch.id) as total_chats,
    AVG(ch.response_time_ms) as avg_response_time_ms,
    MAX(ch.created_at) as last_chat_at,
    u.created_at as user_since
FROM users u
LEFT JOIN companies c ON u.id = c.user_id
LEFT JOIN chat_history ch ON u.id = ch.user_id
GROUP BY u.id, u.username, u.email, u.created_at;

-- Insert a default demo user (password: demo123 - hashed with bcrypt)
-- Note: In production, use proper password hashing!
INSERT INTO users (username, email, password_hash, is_active) 
VALUES ('demo', 'demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEiUM6', TRUE)
ON DUPLICATE KEY UPDATE username=username;
