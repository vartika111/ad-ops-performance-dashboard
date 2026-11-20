@echo off
echo Starting AdPulse 360 Ad Operations Dashboard...
cd /d "%~dp0"
"%LOCALAPPDATA%\Programs\Python\Python311\Scripts\streamlit.exe" run app.py
pause
