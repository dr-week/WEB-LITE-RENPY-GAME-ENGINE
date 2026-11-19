@echo off
REM Opens the native Tauri LOLA Game Launcher (single-instance, silent).
setlocal
set "EXE=%~dp0..\..\development\game-launcher\src-tauri\target\release\lola_game_launcher.exe"

if exist "%EXE%" (
  tasklist /FI "IMAGENAME eq lola_game_launcher.exe" /NH | find /I "lola_game_launcher.exe" >nul
  if not errorlevel 1 exit /b 0
  start "" "%EXE%"
  exit /b 0
)

cd /d "%~dp0"
where pythonw >nul 2>nul
if not errorlevel 1 (
  start "" pythonw "%~dp0game_launcher.pyw"
  exit /b 0
)

call "%~dp0Play LOLA Direct.bat"
