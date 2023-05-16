@echo off

REM Set up environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

REM Start the Flask app
flask run

pause