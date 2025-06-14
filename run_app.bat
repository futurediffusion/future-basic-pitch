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

REM Run the Gradio application with tuned parameters
python app.py --onset-threshold 0.6 --frame-threshold 0.4 --minimum-note-length 200 --minimum-frequency 55 --maximum-frequency 1760 --multiple-pitch-bends

pause
