echo [+] Building Migrations
python manage.py makemigrations

echo [+] Migrating
python manage.py migrate
