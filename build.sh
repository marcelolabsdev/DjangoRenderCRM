#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('ADMIN_USER', 'admin')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username,
        os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
        os.environ.get('ADMIN_PASSWORD', 'Admin123!')
    )
    print('Superusuario creado:', username)
else:
    print('Superusuario ya existe:', username)
"
