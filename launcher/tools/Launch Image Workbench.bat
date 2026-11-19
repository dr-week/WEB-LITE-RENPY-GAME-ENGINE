@echo off
setlocal
set "APP_DIR=%~dp0..\..\development\image-workbench"
set "EXE=%APP_DIR%\src-tauri\target\release\lola_image_workbench.exe"

if exist "%EXE%" if /i not "%~1"=="--dev" (
  echo Starting standalone LOLA Image Workbench...
  start "" /d "%APP_DIR%" "%EXE%"
  exit /b 0
)

cd /d "%APP_DIR%"

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is required to run the auto-updating development window.
  pause
  exit /b 1
)

if not exist "node_modules" (
  echo Installing Image Workbench dependencies...
  call npm install --no-audit --no-fund
  if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
  )
)

echo Starting the native Image Workbench with automatic source updates.
echo Keep this console open while using the development window.
call npm run tauri:dev
if errorlevel 1 (
  echo The auto-updating Image Workbench stopped with an error.
  pause
  exit /b 1
)
