@echo off
REM Direct silent game launch straight into LOLA's Main Menu (no --safe-mode config screen).
setlocal
cd /d "%~dp0"

where pythonw >nul 2>nul
if not errorlevel 1 (
  pythonw -c "import sys; sys.path.insert(0, r'%~dp0'); import game_launcher_core as c; c.launch_game(c.load())"
  exit /b 0
)

set "SDK=C:\RenPy\renpy-8.6.0\renpy-8.6.0-sdk"
for %%I in ("%~dp0..\..") do set "PROJECT=%%~fI"
cd /d "%SDK%"
start "" "%SDK%\lib\py3-windows-x86_64\pythonw.exe" "%SDK%\renpy.py" "%PROJECT%" run
