@echo off
setlocal
set "CHROME_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe"
set "PROFILE_DIR=%LOCALAPPDATA%\LOLA\FlowChromeProfile"
if not exist "%CHROME_EXE%" (
    echo Chrome not found at "%CHROME_EXE%".
    pause
    exit /b 1
)
if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"
echo Launching Chrome with CDP on port 9222 for Google Flow...
start "" "%CHROME_EXE%" --remote-debugging-port=9222 --user-data-dir="%PROFILE_DIR%" "https://flow.google"
