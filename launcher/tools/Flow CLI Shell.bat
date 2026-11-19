@echo off
REM Opens the CLI-Anything LOLA Flow interactive REPL shell.
setlocal
cd /d "%~dp0..\..\developer-tools"
python cli_anything_lola_flow.py
pause
