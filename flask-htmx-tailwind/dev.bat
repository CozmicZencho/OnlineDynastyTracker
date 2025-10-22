@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

REM --- Defaults ---
set "PORT=5000"
set "FLASK_APP=app"

REM --- Read .env (KEY=VALUE; lines starting with # ignored) ---
if exist ".env" (
  for /f "usebackq eol=# tokens=1,2 delims== " %%A in (".env") do (
    if /I "%%A"=="PORT" set "PORT=%%B"
    if /I "%%A"=="FLASK_APP" set "FLASK_APP=%%B"
  )
)

REM --- Trim quotes/spaces ---
set "PORT=!PORT:"=!"
for /f "tokens=* delims= " %%Z in ("!PORT!") do set "PORT=%%Z"
set "FLASK_APP=!FLASK_APP:"=!"
for /f "tokens=* delims= " %%Z in ("!FLASK_APP!") do set "FLASK_APP=%%Z"

echo === Starting Flask backend on http://127.0.0.1:!PORT! (app=!FLASK_APP!) ===
start "Flask" cmd /k "set FLASK_APP=!FLASK_APP!&& .\.venv\Scripts\python.exe -m flask run --port !PORT!"

echo === Starting Tailwind watcher ===
start "Tailwind" cmd /k "npm run tailwind:dev"

echo Servers started. Press any key to close this launcher window.
pause
