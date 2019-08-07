# gunicorn.conf.py
bind = '0.0.0.0:8123'
workers = 6
accesslog = '-'
errorlog = '-'