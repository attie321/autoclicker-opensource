@echo off
pythonw "%~dp0AutoClicker_Pro.py" 2>nul
if errorlevel 1 python "%~dp0AutoClicker_Pro.py"
