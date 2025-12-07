# MySQL Setup Guide for Beginners

This guide will help you install and configure MySQL for the AI Chatbot Assistant application.

## Step 1: Download MySQL

1. Visit the official MySQL website: https://dev.mysql.com/downloads/mysql/
2. Select your operating system (Windows)
3. Download the **MySQL Installer** (recommended: mysql-installer-web-community)

## Step 2: Install MySQL

1. Run the downloaded installer
2. Choose **"Developer Default"** setup type
3. Click **Next** through the installation
4. When prompted, set a **root password** (remember this!)
   - Example: `MySecurePassword123`
5. Complete the installation

## Step 3: Verify Installation

1. Open **Command Prompt** (cmd)
2. Type: `mysql --version`
3. You should see the MySQL version number

## Step 4: Access MySQL

### Option A: Using MySQL Command Line

1. Open **Command Prompt**
2. Type: `mysql -u root -p`
3. Enter your root password when prompted
4. You should see: `mysql>`

### Option B: Using MySQL Workbench (GUI)

1. Open **MySQL Workbench** (installed with MySQL)
2. Click on **Local instance MySQL**
3. Enter your root password
4. You're now connected!

## Step 5: Create the Database

### Using Command Line:

```sql
-- Copy and paste these commands one by one
CREATE DATABASE chatbot_db;
USE chatbot_db;
```

### Using MySQL Workbench:

1. Click **File** → **Open SQL Script**
2. Select `database_schema.sql` from your project folder
3. Click the **Execute** button (lightning bolt icon)

## Step 6: Create Database Tables

1. Navigate to your project folder in Command Prompt:
   ```bash
   cd c:\Users\Hirthick\Videos\SYN
   ```

2. Run the schema file:
   ```bash
   mysql -u root -p chatbot_db < database_schema.sql
   ```

3. Enter your password when prompted

## Step 7: Configure the Application

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file with your settings:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=YourPasswordHere
   DB_NAME=chatbot_db
   GEMINI_API_KEY=your_api_key_here
   ```

## Step 8: Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key
5. Paste it in your `.env` file

## Step 9: Test Database Connection

1. Make sure MySQL is running
2. Run the Flask app:
   ```bash
   python app.py
   ```

3. Visit: http://localhost:5000/test-db
4. You should see: `{"success": true, "message": "Database connection successful"}`

## Common Issues and Solutions

### Issue: "Access denied for user 'root'"
**Solution:** Check your password in the `.env` file

### Issue: "Can't connect to MySQL server"
**Solution:** 
- Make sure MySQL service is running
- Windows: Open Services → Find "MySQL" → Start it
- Or run: `net start MySQL80` (adjust version number)

### Issue: "Unknown database 'chatbot_db'"
**Solution:** Run the CREATE DATABASE command again

### Issue: "Table doesn't exist"
**Solution:** Import the schema file again using the command in Step 6

## Useful MySQL Commands

```sql
-- Show all databases
SHOW DATABASES;

-- Use a database
USE chatbot_db;

-- Show all tables
SHOW TABLES;

-- View table structure
DESCRIBE companies;

-- View data in a table
SELECT * FROM companies;

-- Delete all data from a table
TRUNCATE TABLE chat_history;

-- Drop database (careful!)
DROP DATABASE chatbot_db;
```

## Alternative: Using XAMPP (Easier for Beginners)

If MySQL installation is too complex, you can use XAMPP:

1. Download XAMPP: https://www.apachefriends.org/
2. Install XAMPP
3. Open XAMPP Control Panel
4. Start **MySQL** service
5. Click **Admin** button (opens phpMyAdmin)
6. Create database `chatbot_db`
7. Import `database_schema.sql`

Your `.env` settings for XAMPP:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=chatbot_db
```

## Need Help?

- MySQL Documentation: https://dev.mysql.com/doc/
- MySQL Community: https://forums.mysql.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/mysql

---

**Next Step:** Once MySQL is set up, proceed to the main README.md for running the application!
