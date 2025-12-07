@echo off
echo Creating .env file with your configuration...
echo.

(
echo # MySQL Database Configuration
echo DB_HOST=localhost
echo DB_USER=root
echo DB_PASSWORD=Hirthick#6
echo DB_NAME=chatbot_db
echo.
echo # Google Gemini API Key
echo GEMINI_API_KEY=AIzaSyBzyc_fYj8dy7BW-gEN497pvm5P60XfjHU
echo.
echo # Flask Configuration
echo FLASK_ENV=development
echo FLASK_DEBUG=True
) > .env

echo ✓ .env file created successfully!
echo.
echo Starting the application...
python app.py
