@echo off
echo Installing Mercury AI V1...
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Mercury AI V1 installed successfully.
pause
