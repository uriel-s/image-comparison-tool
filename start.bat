@echo off
echo Starting Image Comparison Tool Web Interface...
echo.

cd /d "%~dp0"

echo Checking dependencies...
pip install -r requirements.txt --quiet

echo Opening web browser interface...
echo Please wait...
echo.

python -m streamlit run gui/streamlit_gui.py --server.port 8501

pause
