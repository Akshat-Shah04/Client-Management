@echo off
echo Running Django project...

:: Navigate to the project directory (Update the path as needed)
cd /d "C:\Users\pathi\Desktop\Client Office\env\ClientManagement" || exit /b

:: Activate the existing virtual environment
call env\Scripts\activate

:: Run the server
python manage.py runserver 0.0.0.0:8000

:: Keep the terminal open until manually closed
pause

:: Deactivate the virtual environment after stopping the server
:: deactivate
:: pause
