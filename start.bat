@echo off
echo ========================================
echo   Email Classifier - Start Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Copying .env.example to .env
    copy .env.example .env
    echo.
    echo Please edit .env file with your Azure OpenAI credentials
    echo Press any key to continue with fallback classifier...
    pause
)

REM Start backend
echo.
echo Starting backend server...
echo Backend will run on http://localhost:8000
echo.
start cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start frontend
echo Starting frontend server...
echo Frontend will run on http://localhost:8080
echo.
start cmd /k "cd frontend && python -m http.server 8080"

REM Wait for frontend to start
timeout /t 2 /nobreak

REM Open browser
echo Opening browser...
start http://localhost:8080

echo.
echo ========================================
echo   Application is running!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in the command windows to stop servers
echo.
pause
