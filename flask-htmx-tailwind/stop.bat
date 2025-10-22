@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

REM --- Default port ---
set "PORT=5000"

REM --- Read PORT from .env if present ---
if exist ".env" (
  for /f "usebackq eol=# tokens=1,2 delims== " %%A in (".env") do (
    if /I "%%A"=="PORT" set "PORT=%%B"
  )
)

REM --- Trim quotes/spaces ---
set "PORT=!PORT:"=!"
for /f "tokens=* delims= " %%Z in ("!PORT!") do set "PORT=%%Z"

echo Stopping Flask (port !PORT!) and Tailwind (node.exe)...

REM Kill whatever is listening on :PORT (LISTENING state)
for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:":!PORT!\>.*LISTENING"') do (
  taskkill /PID %%P /F >nul 2>&1
)

REM Kill Node (Tailwind watcher)
taskkill /IM node.exe /F >nul 2>&1

echo Done.
pause
