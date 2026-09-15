@echo off
title SkillGap AI Launcher
echo ===================================================
echo        Starting SkillGap AI (Full Stack)
echo ===================================================
echo.

cd /d "%~dp0"

:: Check if venv exists, if so activate it
if exist "venv\Scripts\activate.bat" (
    set "PY_CMD=call venv\Scripts\activate.bat && python -m uvicorn backend.main:app --reload --port 8000"
) else (
    set "PY_CMD=python -m uvicorn backend.main:app --reload --port 8000"
)

:: Start Backend in a separate terminal
echo [1/2] Launching Backend on http://localhost:8000 ...
start "SkillGap AI - Backend" cmd /k "%PY_CMD%"

:: Start Frontend in a separate terminal
echo [2/2] Launching Frontend on http://localhost:5173 ...
start "SkillGap AI - Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo Project is running!
echo - Frontend: http://localhost:5173
echo - Backend:  http://localhost:8000
echo - Swagger:  http://localhost:8000/docs
echo.
echo Close the two opened windows anytime to stop the servers.
echo ===================================================
pause
