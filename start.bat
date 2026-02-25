@echo off
REM ============================================================
REM AgriChain — Blockchain Traceability for Sustainable Agriculture
REM Single-command startup script (Windows)
REM ============================================================

echo.
echo  ====================================================
echo    AgriChain - Blockchain Agricultural Traceability
echo  ====================================================
echo.

cd /d "%~dp0"

REM --- Step 1: Python Virtual Environment ---
if not exist "venv" (
    echo [*] Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo [OK] Virtual environment active

REM --- Step 2: Install Dependencies ---
echo [*] Installing dependencies...
pip install --upgrade pip --quiet 2>nul
pip install -r requirements.txt --quiet

REM --- Step 3: Create media directories ---
if not exist "Agriculture\media\products" mkdir "Agriculture\media\products"
if not exist "Agriculture\media\qrcodes" mkdir "Agriculture\media\qrcodes"

REM --- Step 4: Database Setup ---
echo [*] Running database migrations...
cd Agriculture
python manage.py makemigrations AgricultureApp --verbosity 0 2>nul
python manage.py migrate --run-syncdb --verbosity 0

REM --- Step 4b: Seed sample data ---
echo [*] Checking sample data...
python manage.py seed_data

REM --- Step 5: Try Ganache ---
echo.
where ganache-cli >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [*] Starting Ganache blockchain on port 9545...
    start /b ganache-cli -p 9545 --quiet
    timeout /t 2 /nobreak >nul
)

REM --- Step 6: Try ngrok ---
echo.
python -c "import pyngrok" 2>nul
if %ERRORLEVEL% equ 0 (
    echo [*] Starting ngrok tunnel...
    python -c "from pyngrok import ngrok; t=ngrok.connect(8000); print('Public URL:', t.public_url)" 2>nul
)

REM --- Step 7: Start Server ---
echo.
echo  ====================================================
echo    AgriChain Ready!
echo    Local:  http://127.0.0.1:8000
echo    Admin:  admin / admin
echo  ====================================================
echo.
echo  Press Ctrl+C to stop the server
echo.

python manage.py runserver 0.0.0.0:8000
