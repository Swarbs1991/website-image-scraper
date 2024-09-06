@echo off

:: Check if Python 3 is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo "Python 3 not found. Please install Python 3 from https://www.python.org/downloads/"
    exit /b
)

:: Install the required libraries
pip install -r requirements.txt

echo "Dependencies installed successfully!"
pause
