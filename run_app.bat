@echo off
REM Navigate to script directory
cd /d %~dp0

REM Create virtual environment if not already present
if not exist venv (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip and install dependencies
pip install --upgrade pip
pip install basic-pitch gradio

REM Run the Gradio application
python app.py

pause
