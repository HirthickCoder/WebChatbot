@echo off
echo ========================================
echo AI Chatbot Assistant - Setup Script
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed successfully!
echo.

echo Step 2: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file
    echo.
    echo IMPORTANT: Please edit .env file and add:
    echo   1. Your MySQL password
    echo   2. Your Gemini API key from https://makersuite.google.com/app/apikey
    echo.
    pause
) else (
    echo ✓ .env file already exists
)
echo.

echo Step 3: Testing database connection...
python -c "import database; conn = database.get_connection(); print('✓ Database connection successful!' if conn else '✗ Database connection failed!')"
echo.

echo Step 4: Creating database tables...
python -c "import database; database.create_tables(); print('✓ Tables created successfully!')"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure MySQL is running
echo 2. Edit .env file with your credentials
echo 3. Run: python app.py
echo 4. Open index.html in your browser
echo.
pause
