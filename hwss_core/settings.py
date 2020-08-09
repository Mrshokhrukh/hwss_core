import os
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARN",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logfile.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARN",
            "propagate": True,
        },
    },
}


CREDENTIALS = {
    "API_KEY": "Rie82o_SERTZEcb8dZbstH2fzJEa",
    "API_SECRET": "Y_drXbOABoHtJ0iII0yzplqzm98a",
    "TOKEN_URL": "https://sso.tech.gov.bt/oauth2/token",
    "API_URL": "https://datahub-apim.tech.gov.bt/dcrc_citizen_details_api/1.0.0/citizendetails/",
    "EMIS_STUDENT_API": "https://datahub-apim.tech.gov.bt/moe_emisinformationapi/1.0.0/studentdetails/",
    "EMIS_STAFF_API": "https://datahub-apim.tech.gov.bt/moe_emisinformationapi/1.0.0/staffdetails/",
    "RCSC_API": "https://datahub-apim.tech.gov.bt/rcsc_zestemployeedetailserviceapi/1.0.0/employeedetailbycid/",
}


INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps module
    "access",
    "measurement",
    "reporting",
    "monitoring",
    "settings_module",
    "screening",
    "gyalsung_users",
    # 3rd party apps
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "import_export",
    "django_quill",
]

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
            os.path.join(BASE_DIR, "venv/Lib/site-packages/import_export/templates"),
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
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("SQLITE_PATH", BASE_DIR / "db.sqlite3"),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.postgresql'),
#         'NAME': config('DATABASE_NAME', default='hwss_core_db'),
#         'USER': config('DATABASE_USER', default='hwss-root'),
#         'PASSWORD': config('DATABASE_PASSWORD', default='hwss@2024'),
#         'HOST': config('DATABASE_HOST', default='172.30.85.156'),
#         'PORT': config('DATABASE_PORT', default='5432'),
#         'OPTIONS': {
#             'sslmode': 'disable',
#         },
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'hwss_core_db',
#         'USER': 'hwss-root',
#         'PASSWORD': 'hwss@2024',
#         'HOST': 'localhost',
#         'PORT': '5432',
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

TIME_ZONE = "Asia/Thimphu"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "access.CustomUser"

STATIC_URL = "/api/core/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/api/core/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

ASGI_APPLICATION = "hwss_core.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

COMMON_ORIGINS = [
    "https://thepemasystem.gov.bt",
    "http://thepemasystem.gov.bt",
    "http://localhost",
    "http://localhost:5173",
    "http://172.30.84.164:8123",
]

# Add a regex pattern for the IP range
IP_RANGE_PATTERN = r"^https?://172\.30\.84\.\d+(?::\d+)?$"

# CORS settings
# CORS_ALLOWED_ORIGINS = COMMON_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_PREFLIGHT_MAX_AGE = 86400

CORS_ORIGIN_REGEX_WHITELIST = [
    IP_RANGE_PATTERN,
]
CORS_ORIGIN_WHITELIST = COMMON_ORIGINS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CROSS_ORIGIN_OPENER_POLICY = "unsafe-none"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "SAMEORIGIN"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8123",
    "https://thepemasystem.gov.bt",
    "http://thepemasystem.gov.bt",
    "http://localhost",
    "http://172.30.84.165",
    "http://172.30.84.164:8123",
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_DOMAIN = None

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_DEBUG = True
DEFAULT_FROM_EMAIL = "PEMA System <noreply@thepemasystem.gov.bt>"
DEFAULT_FROM_NAME = "PEMA System"
CONTACT_EMAIL = "noreply@thepemasystem.gov.bt"
FRONTEND_URL = "https://thepemasystem.gov.bt"

# Use database for session storage
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Store sessions in the database

# # Session cookie settings
# SESSION_COOKIE_AGE = 604800
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SAMESITE = 'Lax'
# SESSION_COOKIE_DOMAIN = '.thepemasystem.gov.bt'
