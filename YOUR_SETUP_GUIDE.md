# Your Personal Setup - Hirthick

## ✅ MySQL Password Set!
Your MySQL root password: `Hirthick#6`

---

## 📋 Next Steps (After MySQL Installation Completes):

### Step 1: Create .env File (1 minute)

1. Open Command Prompt and run:
   ```bash
   cd c:\Users\Hirthick\Videos\SYN
   copy .env.example .env
   ```

2. Open `.env` file in Notepad:
   ```bash
   notepad .env
   ```

3. The file will look like this - **ONLY change the Gemini API key line**:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=Hirthick#6          ← Already correct!
   DB_NAME=chatbot_db
   
   GEMINI_API_KEY=PUT_YOUR_KEY_HERE  ← Change this in Step 2
   
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

4. Save and close

---

### Step 2: Get Gemini API Key (2 minutes)

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with Google
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSyXXXXXXXXXXXXXX`)
5. Open `.env` again and paste it:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXX
   ```
6. Save

---

### Step 3: Create Database (2 minutes)

**Option A: Using MySQL Workbench (Easier)**

1. Open **MySQL Workbench** (search in Start menu)
2. Click **"Local instance MySQL80"**
3. Enter password: `Hirthick#6`
4. In the SQL editor, paste and run:
   ```sql
   CREATE DATABASE chatbot_db;
   ```
5. Click **File** → **Open SQL Script**
6. Select: `c:\Users\Hirthick\Videos\SYN\database_schema.sql`
7. Click **Execute** (⚡ icon)
8. Done! ✅

**Option B: Using Command Line**

```bash
cd c:\Users\Hirthick\Videos\SYN
mysql -u root -p
# Enter password: Hirthick#6
CREATE DATABASE chatbot_db;
SOURCE database_schema.sql;
exit
```

---

### Step 4: Install Python Packages (2 minutes)

```bash
cd c:\Users\Hirthick\Videos\SYN
pip install -r requirements.txt
```

Wait for installation to complete.

---

### Step 5: Start the Application! (1 minute)

```bash
python app.py
```

You should see:
```
Initializing database...
Database tables created successfully!
Starting Flask server...
* Running on http://127.0.0.1:5000
```

**Keep this window open!**

---

### Step 6: Open Frontend (1 minute)

1. Open File Explorer
2. Go to: `c:\Users\Hirthick\Videos\SYN`
3. Double-click `index.html`
4. It will open in your browser

---

### Step 7: Test Your Chatbot! 🎉

1. **Company Name**: `Google`
2. **Website URL**: `https://www.google.com`
3. Click **"Create Chatbot"**
4. Wait 5-10 seconds
5. Ask: `What does this company do?`
6. Get instant AI response! ✅

---

## 🔧 Quick Commands Reference

```bash
# Navigate to project
cd c:\Users\Hirthick\Videos\SYN

# Create .env file
copy .env.example .env

# Install packages
pip install -r requirements.txt

# Start MySQL (if not running)
net start MySQL80

# Start Flask server
python app.py

# Test database connection
python -c "import database; print('✓ Connected!' if database.get_connection() else '✗ Failed')"
```

---

## ⚠️ Troubleshooting

**Can't connect to database?**
- Check MySQL is running: Services → MySQL80 → Start
- Verify password in `.env` is: `Hirthick#6`

**AI not working?**
- Make sure you added Gemini API key to `.env`
- Restart Flask: Ctrl+C, then `python app.py`

**Port 5000 in use?**
- Close other programs
- Or change port in `app.py` to 5001

---

## 📞 Need Help?

Check these files:
- `README.md` - Full documentation
- `MYSQL_SETUP_GUIDE.md` - MySQL help
- `COMPLETE_SETUP_GUIDE.md` - Detailed steps

---

**Your MySQL password is set! Complete the MySQL installation, then follow the steps above.** 🚀
