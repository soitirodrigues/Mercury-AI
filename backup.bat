@echo off
echo Backing up data...
if not exist "backups" mkdir "backups"
set backup_dir=backups\data_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
mkdir "%backup_dir%"
xcopy /E /I /Y "data" "%backup_dir%"
echo Backup completed to %backup_dir%.
pause
