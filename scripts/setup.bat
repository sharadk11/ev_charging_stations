@echo off
echo Setting up EV Charging Station Map Application...
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file with your database credentials and API keys
    echo Press any key after editing .env file...
    pause
)

echo.
echo Step 3: Setting up database...
echo Make sure PostgreSQL is running and you have created the database
echo Run the following command manually:
echo psql -U postgres -f database/init.sql
echo.
pause

echo.
echo Step 4: Running initial data collection...
cd data-pipeline
python data_collector.py
cd ..

echo.
echo Step 5: Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Setup complete! 
echo.
echo To start the application:
echo 1. Start the backend: python backend/main.py
echo 2. Start the frontend: cd frontend && npm start
echo 3. Start data pipeline: python data-pipeline/scheduler.py
echo.
pause