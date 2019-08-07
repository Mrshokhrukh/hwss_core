#!/bin/bash

# Activate virtual environment
. /app/venv/bin/activate

# Run migrations
python manage.py migrate

# Start Gunicorn
gunicorn --config /app/gunicorn.conf.py hwss_core.wsgi:application

# Start Nginx
nginx -g 'daemon off;'
