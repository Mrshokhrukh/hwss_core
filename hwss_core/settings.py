from pathlib import Path
import os
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-h713=ks4vm_*km8t1uh85%jb_@!pt7%k$z3wq9nxh)wglf%=n#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.30.3.5', 'localhost', '127.0.0.1']


CREDENTIALS = {
    'API_KEY': config('CONSUMER_KEY'),
    'API_SECRET': config('CONSUMER_SECRET'),
    'TOKEN_URL': config('TOKEN_URL'),
    'API_URL': config('API_URL'),
    'EMIS_STUDENT_API': config('EMIS_STUDENT_API'),
    'EMIS_STAFF_API': config('EMIS_STAFF_API'),
    'RCSC_API': config('RCSC_API'),
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'access',
    'measurement',
    'reporting',
    'monitoring',
    'settings_module',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
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
        "DIRS": [],
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
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



AUTH_USER_MODEL = 'access.CustomUser'


# DCRC_API_BASE_URL = 'https://staging-datahub-apim.dit.gov.bt/dcrc_citizen_details_api/1.0.0' #DCRC
DCRC_API_BASE_URL = 'https://staging-datahub-apim.dit.gov.bt/rcsc_zestemployeedetailserviceapi/1.0.0/employeedetailbycid' #RCSC
# DCRC_API_BASE_URL = 'https://staging-datahub-apim.dit.gov.bt/moe_emisinformationapi/1.0.0/staffdetails' #EMIS COUNSELLOR
# DCRC_API_BASE_URL = 'https://staging-datahub-apim.dit.gov.bt/moe_emisinformationapi/1.0.0/studentdetails/' #EMIS STUDENT
DCRC_TOKEN_URL = 'https://stg-sso.dit.gov.bt/oauth2/token'
DCRC_CONSUMER_KEY = 'ScC63jo40LjxifHweyLUR6IVto0a'
DCRC_CONSUMER_SECRET = 'jk6jLebfES42oYmf8YuFNuMFpTUa'


CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     'http://127.0.0.1:5173',
# ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')