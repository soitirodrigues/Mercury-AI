@echo off
echo Restoring from latest backup...
set "latest_backup="
for /f "delims=" %%i in ('dir /b /ad /od backups\data_*') do set "latest_backup=backups\%%i"
if "%latest_backup%"=="" (
    echo No backups found.
    pause
    exit /b
)
echo Restoring from: %latest_backup%
xcopy /E /I /Y "%latest_backup%" "data"
echo Restore completed.
pause
