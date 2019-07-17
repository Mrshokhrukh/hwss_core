#!/bin/sh

# Exit script on error
set -e

# Set default values for database connection
POSTGRES_HOST=${POSTGRES_HOST:-172.30.85.156}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

# Function to wait for the database
wait_for_db() {
  echo "Waiting for database at $POSTGRES_HOST:$POSTGRES_PORT..."
  while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 1
  done
  echo "Database started"
}

# Wait for the database to be available
wait_for_db

# Set default values for superuser
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-uhollica666}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-ujwalpradhan@druksmart.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-Caelen@0312}

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created successfully');
else:
    print('Superuser already exists');
"

# Start Gunicorn
echo "Starting Gunicorn..."
exec "$@"