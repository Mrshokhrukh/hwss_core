import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-w+%up+l9l$-lt@izmje9n5b^sf9^2(2tuzmk7*+m=m9d04z#85"

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARN',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logfile.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARN',
            'propagate': True,
        },
    },
}


CREDENTIALS = {
    'API_KEY': 'ZtXTsAHXljLQkzddM2Al1BKx6kwa',
    'API_SECRET': 'df5eVQe7Q2sNe9tfZ4Ai90FMsHca',
    'TOKEN_URL': 'https://sso.dit.gov.bt/oauth2/token',
    'API_URL': 'https://datahub-apim.dit.gov.bt/dcrc_citizen_details_api/1.0.0/citizendetails/',
    'EMIS_STUDENT_API': 'https://datahub-apim.dit.gov.bt/moe_emisinformationapi/1.0.0/studentdetails/',
    'EMIS_STAFF_API': 'https://datahub-apim.dit.gov.bt/moe_emisinformationapi/1.0.0/staffdetails/',
    'RCSC_API': 'https://datahub-apim.dit.gov.bt/rcsc_zestemployeedetailserviceapi/1.0.0/employeedetailbycid/',
}


INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps module
    'access',
    'measurement',
    'reporting',
    'monitoring',
    'settings_module',
    'screening',
    'gyalsung_users',

    # 3rd party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'import_export',
    'django_quill'
]


X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hwss_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'venv/Lib/site-packages/import_export/templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hwss_core.wsgi.application"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}



# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('SQLITE_PATH', BASE_DIR / 'db.sqlite3'),
    }
}

# pgadmin production
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': os.getenv('POSTGRES_PORT', '5432'),
#     }
# }

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'),
#         conn_max_age=600,
#         ssl_require=False
#     )
# }

# for pgadmin local
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'hwss_prod_db',
#         'USER': 'root',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'access.CustomUser'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ASGI_APPLICATION = 'hwss_core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

COMMON_ORIGINS = [
    'https://thepemasystem.gov.bt',
    'http://thepemasystem.gov.bt',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8888',
    'http://localhost:8888',
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    # production ips
    'https://172.30.84.154',
    'http://172.30.84.154',
    'https://172.30.84.155',
    'http://172.30.84.155',
    'https://172.30.84.156',
    'http://172.30.84.156',
    'https://172.30.84.157',
    'http://172.30.84.157',
    'https://172.30.84.158',
    'http://172.30.84.158',
    'https://172.30.84.159',
    'http://172.30.84.159',
    'https://172.30.84.159',
    'http://172.30.84.159',
]

# CORS settings
CORS_ALLOWED_ORIGINS = COMMON_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_PREFLIGHT_MAX_AGE = 86400

CSRF_TRUSTED_ORIGINS = COMMON_ORIGINS

CORS_ORIGIN_WHITELIST = COMMON_ORIGINS