@echo off
:: install.bat - for Windows

echo Starting installation for Kimi Auto Mail Tool...

:: Step 1: Create and activate a virtual environment
echo Creating virtual environment...
python -m venv venv
call .\venv\Scripts\activate.bat

echo Virtual environment activated.

:: Step 2: Install Python dependencies
echo Installing Python dependencies from requirements.txt...
pip install -r .\code\requirements.txt

:: Step 3: Install Playwright browsers
echo Installing Playwright browsers (this might take a while)...
playwright install

echo Installation complete!
echo Please rename config.py.template to config.py and fill in your details.
echo To run the script, first activate the virtual environment by running: .\venv\Scripts\activate.bat
echo Then run the main script with: python main.py

pause
