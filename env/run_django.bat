@echo off
:: Display the virtual environment activation
cd /d C:\Users\pathi\Desktop\Client Office
call .\env\Scripts\activate

:: Navigate to the project directory
cd env\ClientManagement

:: Apply migrations and start the Django server
:: pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

:: Prevent the window from closing
pause
