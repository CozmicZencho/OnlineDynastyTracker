@echo off
cd /d "%~dp0"

echo === Starting Flask backend ===
start "Flask" cmd /k ".\.venv\Scripts\python.exe -m flask run"

echo === Starting Tailwind watcher ===
start "Tailwind" cmd /k "npm run tailwind:dev"

echo Servers started.
pause
