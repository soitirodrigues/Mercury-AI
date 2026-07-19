@echo off
echo Running Healthcheck for Mercury AI V1...
call .venv\Scripts\activate
python -m pytest tests/
pause
