# django/Dockerfile
FROM python:3.11-alpine3.19

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libpq-dev \
    && apk add --no-cache postgresql-client \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del .build-deps

# Copy application code
COPY . /app/

# Set the script as executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Adjust permissions for static files
RUN chmod -R 755 /app/staticfiles

# Expose port 8000
EXPOSE 8000

# Set entrypoint and default command
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "hwss_core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "6"]
