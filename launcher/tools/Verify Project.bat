@echo off
REM Runs unified automated verification + all 53 Python unit tests + Ren'Py lint.
setlocal
set "SDK=C:\RenPy\renpy-8.6.0\renpy-8.6.0-sdk"
for %%I in ("%~dp0..\..") do set "PROJECT=%%~fI"

cd /d "%PROJECT%"
set "PYTHONPATH=%PROJECT%\developer-tools;%PROJECT%"

python "%PROJECT%\developer-tools\checks\run_all_checks.py"
if errorlevel 1 (
  echo Pre-launch checks failed.
  pause
  exit /b 1
)

python -m unittest discover -s developer-tools/tests -p "test_*.py"
if errorlevel 1 (
  echo Unit tests failed.
  pause
  exit /b 1
)

"%SDK%\lib\py3-windows-x86_64\python.exe" "%SDK%\renpy.py" "%PROJECT%" lint
pause
