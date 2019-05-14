from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-h713=ks4vm_*km8t1uh85%jb_@!pt7%k$z3wq9nxh)wglf%=n#"

DEBUG = True

ALLOWED_HOSTS = ['172.30.3.5', 'localhost', '127.0.0.1']

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARN',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_DIR, 'logfile.log'),
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


# Application definition

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
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hwss_core',
#         'USER': 'root',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'access.CustomUser'

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ASGI_APPLICATION = 'hwss_core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Define common origins
COMMON_ORIGINS = [
    'https://thepemasystem.gov.bt',
    'http://thepemasystem.gov.bt',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'https://172.30.84.97',
    'http://172.30.84.97',
    'https://103.252.84.46',
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
