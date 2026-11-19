@echo off
REM Runs pre-flight static asset/symbol check + Ren'Py lint check.
setlocal
set "SDK=C:\RenPy\renpy-8.6.0\renpy-8.6.0-sdk"
for %%I in ("%~dp0..\..") do set "PROJECT=%%~fI"
python "%PROJECT%\developer-tools\checks\verify_game_assets.py"
if errorlevel 1 (
  pause
  exit /b 1
)
"%SDK%\lib\py3-windows-x86_64\python.exe" "%SDK%\renpy.py" "%PROJECT%" lint
pause
