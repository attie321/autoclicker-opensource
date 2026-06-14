@echo off
setlocal EnableDelayedExpansion
title AutoClicker Pro - Installer
color 0A
mode con: cols=60 lines=30

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║        AutoClicker Pro - Installer           ║
echo  ║  NL / EN / DE / FR / ES / TR                ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: ── Stap 1: Python checken ──────────────────────
echo  [1/4] Controleren Python installatie...
python --version >nul 2>&1
if %errorlevel% NEQ 0 (
    echo.
    echo  [FOUT] Python niet gevonden!
    echo.
    echo  Python is gratis en vereist voor de app.
    echo  Download het nu automatisch...
    echo.
    echo  BELANGRIJK: Vink "Add Python to PATH" aan!
    echo.
    pause
    start https://www.python.org/downloads/
    echo.
    echo  Installeer Python en start INSTALL.bat opnieuw.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  [OK] %%v gevonden.
echo.

:: ── Stap 2: pip packages ────────────────────────
echo  [2/4] Installeren packages (pynput, pyautogui)...
python -m pip install pynput pyautogui --quiet --disable-pip-version-check 2>nul
if %errorlevel% NEQ 0 (
    echo  [!] Poging 2 met --user flag...
    python -m pip install pynput pyautogui --user --quiet 2>nul
)
echo  [OK] Packages gereed.
echo.

:: ── Stap 3: VBS launcher aanmaken ───────────────
echo  [3/4] Launcher aanmaken...
set "DIR=%~dp0"
set "VBS=%DIR%Start_Silent.vbs"
set "PY=%DIR%AutoClicker_Pro.py"

(
echo Dim dir
echo dir = Left^(WScript.ScriptFullName, InStrRev^(WScript.ScriptFullName, "\"^)^)
echo CreateObject^("WScript.Shell"^).Run "pythonw """ ^& dir ^& "AutoClicker_Pro.py""", 0, False
) > "%VBS%"

echo  [OK] Launcher aangemaakt.
echo.

:: ── Stap 4: Bureaublad snelkoppeling ────────────
echo  [4/4] Snelkoppeling aanmaken op bureaublad...
set "DESK=%USERPROFILE%\Desktop"
set "LNK=%DESK%\AutoClicker Pro.lnk"

powershell -NoProfile -Command ^
  "try { $ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%LNK%'); $s.TargetPath = 'wscript.exe'; $s.Arguments = '\""%VBS%\"" '; $s.WorkingDirectory = '%DIR%'; $s.Description = 'AutoClicker Pro'; $s.IconLocation = 'shell32.dll,15'; $s.Save(); Write-Host '[OK] Snelkoppeling aangemaakt.' } catch { Write-Host '[!] Snelkoppeling mislukt (niet kritiek).' }" 2>nul

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║            Installatie voltooid!             ║
echo  ║                                              ║
echo  ║  Start de app via:                           ║
echo  ║  • Bureaublad snelkoppeling                  ║
echo  ║  • Of dubbelklik op Start_Silent.vbs         ║
echo  ║                                              ║
echo  ║  Taal kiezen in de app (bovenaan links)      ║
echo  ║  NL / EN / DE / FR / ES / TR                ║
echo  ╚══════════════════════════════════════════════╝
echo.
echo  De app start nu op...
timeout /t 2 /nobreak >nul
start "" wscript "%VBS%"
echo.
pause
