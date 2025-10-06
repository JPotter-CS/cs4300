#!/usr/bin/env bash
set -o errexit

echo "Running requirements.txt"
pip install -r requirements.txt

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Running migrations"
python manage.py migrate

echo "Creating superuser if it doesn't exist"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "Creating sample data..."
python manage.py create_sample_data || echo "Sample data command not available or already exists"

echo "Build completed"
