#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

python manage.py makemigrations
python manage.py migrate
#echo "from helios_auth.models import User; User.objects.create(user_type='google',user_id='ben@adida.net', info={'name':'Ben Adida'})" | python manage.py shell
echo "from helios_auth.auth_systems.password import create_user; create_user('admin', 'password')" | python manage.py shell || true

gunicorn wsgi:application -b 0.0.0.0:8000 -w 8