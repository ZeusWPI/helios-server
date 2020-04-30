#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

python manage.py makemigrations
python manage.py migrate
#echo "from helios_auth.models import User; User.objects.create(user_type='google',user_id='ben@adida.net', info={'name':'Ben Adida'})" | python manage.py shell
echo "from helios_auth.models import User; User.update_or_create(user_type='password', user_id=0, name='admin', info={'password': 'password', 'email': 'admin@zeus.ugent.be'})" | python manage.py shell || true

gunicorn wsgi:application -b 0.0.0.0:8000 -w 8
