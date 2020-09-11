# Stage 1: Build
FROM python:3.11.9-alpine3.18 as build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev postgresql-dev build-base bash

# Set work directory
WORKDIR /app

# Install and configure virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Stage 2: Final
FROM python:3.11.9-alpine3.18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
RUN apk update \
    && apk add --no-cache bash libpq

# Set work directory
WORKDIR /app

# Copy virtual environment and application
COPY --from=build /app/venv /app/venv
COPY . /app

# Create and activate virtual environment
RUN python -m venv /app/venv \
    && . /app/venv/bin/activate

# Configure Gunicorn
RUN pip install gunicorn
COPY gunicorn.conf.py /app/gunicorn.conf.py

RUN echo -e "https://dl-cdn.alpinelinux.org/alpine/v3.18/main\nhttps://dl-cdn.alpinelinux.org/alpine/v3.18/community" > /etc/apk/repositories

# Install Nginx
RUN apk add --no-cache nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 8123
# Append to /etc/hosts at container runtime
CMD sh -c 'echo "172.30.78.43 sso.tech.gov.bt" >> /etc/hosts && echo "172.30.78.42 datahub-apim.tech.gov.bt" >> /etc/hosts && nginx && gunicorn --config /app/gunicorn.conf.py hwss_core.wsgi:application'
