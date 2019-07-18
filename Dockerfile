FROM python:3.11.9-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=hwss_core.settings

WORKDIR /app

COPY requirements.txt /app/

RUN set -ex && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/' /etc/apk/repositories && \
    for i in 1 2 3; do apk update && break || sleep 5; done && \
    for i in 1 2 3; do apk add --no-cache --virtual .build-deps gcc musl-dev && break || sleep 5; done && \
    for i in 1 2 3; do apk add --no-cache netcat-openbsd nginx && break || sleep 5; done && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY . /app/

RUN mkdir -p /app/data

RUN python manage.py collectstatic --noinput

RUN rm -f /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Create a directory for static files
RUN mkdir -p /app/staticfiles

EXPOSE 8888

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8888/healthz || exit 1

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn --workers=6 --bind=unix:/tmp/gunicorn.sock hwss_core.wsgi:application & nginx -g 'daemon off;'"]