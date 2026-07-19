@echo off
echo Updating Mercury AI V1...
call .venv\Scripts\activate
pip install -r requirements.txt --upgrade
echo Mercury AI V1 updated successfully.
pause
