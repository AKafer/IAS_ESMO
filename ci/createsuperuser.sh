#!/bin/bash

docker exec esmo_app python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${ADMIN_LOGIN}').exists():
    User.objects.create_superuser('${ADMIN_LOGIN}', '${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')
    print('Superuser created.')
else:
    print('Superuser already exists, skipping.')
"
