#!/bin/bash

# Activate virtual environment
. /app/venv/bin/activate

# Run migrations
# Enable the below 2 only if there has been changes in the models else no need to run
# python manage.py makemigrations
# python manage.py migrate

# Start Gunicorn
gunicorn --config /app/gunicorn.conf.py hwss_core.wsgi:application

# Start Nginx
nginx -g 'daemon off;'
