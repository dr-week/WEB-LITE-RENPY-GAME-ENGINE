@echo off
setlocal
set "APP_DIR=%~dp0..\..\development\image-workbench"
cd /d "%APP_DIR%"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is required to build the release app.
  pause
  exit /b 1
)
if not exist "node_modules" (
  call npm install --no-audit --no-fund
  if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
  )
)
call npm run tauri:build
if errorlevel 1 (
  echo The release app could not be built. Check Node.js and Rust setup.
  pause
  exit /b 1
)
echo Release executable created at:
echo %APP_DIR%\src-tauri\target\release\lola_image_workbench.exe
