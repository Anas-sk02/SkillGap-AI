@echo off
title SkillGap AI First-Time Setup
echo ===================================================
echo        SkillGap AI - First-Time Setup
echo ===================================================
echo.

cd /d "%~dp0"

echo [1/4] Creating Python virtual environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creating virtual environment. Ensure Python is installed and in PATH.
    pause
    exit /b %errorlevel%
)

call venv\Scripts\activate.bat

echo.
echo [2/4] Installing Python requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python requirements.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] Preparing dataset and training ML model artifacts...
python -m ml.preprocessing
python -m ml.train_model
if %errorlevel% neq 0 (
    echo Error training ML model.
    pause
    exit /b %errorlevel%
)

echo.
echo [4/4] Installing Frontend npm packages...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Error installing frontend dependencies.
    pause
    exit /b %errorlevel%
)
cd ..

echo.
echo ===================================================
echo Setup Complete!
echo You can now double-click start.bat to run the project anytime.
echo ===================================================
pause
