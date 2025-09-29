@echo off
title NYC Trip Planner - Web Server

echo 🗽 NYC Family Trip Planner - Starting Web Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
for /f "tokens=*" %%i in ('python --version') do echo    %%i

REM Check if markdown is installed
python -c "import markdown" >nul 2>&1
if errorlevel 1 (
    echo 📦 Markdown library not found (optional for better formatting)
    echo.
    set /p install="   Install markdown for enhanced formatting? (y/n): "
    if /i "%install%"=="y" (
        echo 📦 Installing markdown...
        pip install markdown
        if errorlevel 0 (
            echo ✅ Markdown installed successfully!
        ) else (
            echo ⚠️  Markdown installation failed, continuing with basic formatting...
        )
    ) else (
        echo ⏭️  Skipping markdown installation (basic formatting will be used)
    )
) else (
    echo ✅ Markdown library found - enhanced formatting enabled!
)

echo.
echo 🚀 Starting server...
echo 📍 Your documents will be available at: http://localhost:8080
echo 📱 Mobile access: Find your computer's IP address and use http://[your-ip]:8080
echo.
echo 💡 Tip: Bookmark http://localhost:8080 for easy access!
echo 🛑 Press Ctrl+C to stop the server when done
echo.
echo ────────────────────────────────────────────────────────

REM Start the Python server
python serve_docs.py

echo.
echo 👋 Server stopped. Thanks for planning your NYC trip!
pause

