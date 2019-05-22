#!/bin/sh

# Exit script on error
set -e

# Wait for the database to be available
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database started"

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
else:
    print('Superuser already exists');
"

# Start Gunicorn
exec "$@"
