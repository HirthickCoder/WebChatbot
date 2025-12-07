# Quick Start Guide - AI Chatbot Assistant

Follow these steps to get your chatbot running in minutes!

## Step 1: Install MySQL (if not already installed)

### Option A: MySQL Installer (Recommended)
1. Download from: https://dev.mysql.com/downloads/mysql/
2. Run installer and choose "Developer Default"
3. Set root password (remember it!)

### Option B: XAMPP (Easier for beginners)
1. Download from: https://www.apachefriends.org/
2. Install and start MySQL from XAMPP Control Panel

## Step 2: Create Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE chatbot_db;
```

Or use the provided script:
```bash
mysql -u root -p < database_schema.sql
```

## Step 3: Install Python Dependencies

```bash
cd c:\Users\Hirthick\Videos\SYN
pip install -r requirements.txt
```

## Step 4: Configure Environment

1. Copy the example file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` with your details:
   - Set your MySQL password
   - Add your Gemini API key from: https://makersuite.google.com/app/apikey

## Step 5: Run the Application

1. Start the backend:
   ```bash
   python app.py
   ```

2. Open `index.html` in your browser

## Step 6: Test It!

1. Enter a company name: "Google"
2. Enter website URL: "https://www.google.com"
3. Click "Create Chatbot"
4. Ask questions like "What does this company do?"

## Troubleshooting

### Can't connect to database?
- Make sure MySQL is running
- Check your password in `.env`

### AI not responding?
- Get API key from: https://makersuite.google.com/app/apikey
- Add it to `.env` file
- Restart Flask server

### Website scraping failed?
- Make sure URL starts with `https://`
- Some websites block scrapers
- Try a different website

## Need More Help?

See the full documentation in [README.md](README.md)
