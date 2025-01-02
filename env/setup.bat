@echo off
echo Setting up Django project...

:: Navigate to the project directory (Update the path as needed)
cd /d "C:\Users\pathi\Desktop\Client Office\env\ClientManagement" || exit /b

:: Check if Python and pip are installed
python --version >nul 2>&1 || (
    echo Python is not installed. Please install Python and add it to PATH.
    pause
    exit /b
)
pip --version >nul 2>&1 || (
    echo pip is not installed. Please install pip.
    pause
    exit /b
)

:: Activate the existing virtual environment
call env\Scripts\activate

:: Install dependencies from requirements.txt (outside the env folder)
pip install --upgrade pip
pip install -r "C:\Users\pathi\Desktop\Client Office\env\ClientManagement\requirements.txt"

:: Apply migrations
python manage.py migrate

:: Collect static files
python manage.py collectstatic --noinput

:: Deactivate the virtual environment
deactivate

echo Setup complete.
pause
