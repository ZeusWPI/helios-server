#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.
sleep 5
python manage.py makemigrations
python manage.py migrate

echo "from helios_auth.models import User; u = User.update_or_create(user_type='password', user_id='admin', name='admin', info={'password': '${ADMIN_PASSWORD}', 'email': '${ADMIN_EMAIL}'}); u.admin_p = True; u.save()" | python manage.py shell || true

gunicorn wsgi:application -b 0.0.0.0:8000 -w 8
