"""
Django settings for energy_site project.
"""

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

# ----------------------
# BASE DIR
# ----------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------
# SECURITY / ENV
# ----------------------
# Render/Prod: set SECRET_KEY in Environment
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-secret-key")

# Render: set DEBUG="0" (or "False")
DEBUG = os.environ.get("DEBUG", "1").lower() in ("1", "true", "yes", "y")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "alterhol.com",
    "www.alterhol.com",
    "alterhol.com.ua",
    "www.alterhol.com.ua",
    "energy-site.onrender.com",
]

# Якщо на Render інколи приходить host без www/з іншим доменом —
# можна дозволити все (не рекомендую), тому залишаємо чіткий список.


# ----------------------
# SITE / DOMAIN (для sitemap)
# ----------------------
SITE_ID = int(os.environ.get("SITE_ID", "1"))
SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "https://alterhol.com.ua")


# ----------------------
# UPLOADCARE (виносимо в ENV)
# ----------------------
# ----------------------
# UPLOADCARE (виправлено)
# ----------------------
UPLOADCARE = {
    # Бібліотека очікує саме 'pub_key'
    "pub_key": os.environ.get("UPLOADCARE_PUB_KEY", "36a3b067e0bb8abe769c"),
    # Бібліотека очікує саме 'secret'
    "secret": os.environ.get("UPLOADCARE_SECRET_KEY", "67df6d9ae083fc6a1ddb"),
}

# Важливо для коректної роботи сховища
UPLOADCARE_STORAGE = "pyuploadcare.dj.storage.UploadcareStorage"
DEFAULT_FILE_STORAGE = UPLOADCARE_STORAGE
# ----------------------
# INSTALLED APPS
# ----------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    'cloudinary_storage',
    'cloudinary',

    # third-party
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "rest_framework_simplejwt",
    "pyuploadcare.dj",

    # local apps
    "main",
    "accounts",
]


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dm4dhfqmk',
    'API_KEY': '544226813353368',
    'API_SECRET': 'JH887nTIkxZkBuUU9g5g3CYqMJI'
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
# ----------------------
# MIDDLEWARE
# ----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",  # має бути вище CommonMiddleware

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ----------------------
# URLS / WSGI
# ----------------------
ROOT_URLCONF = "energy_site.urls"
WSGI_APPLICATION = "energy_site.wsgi.application"


# ----------------------
# TEMPLATES
# ----------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "main" / "templates"],
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


# ----------------------
# DATABASE
# ----------------------
# Render gives DATABASE_URL automatically when you attach a Postgres.
# Locally falls back to sqlite.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# ----------------------
# PASSWORD VALIDATION
# ----------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ----------------------
# INTERNATIONALIZATION
# ----------------------
LANGUAGE_CODE = "uk"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ----------------------
# STATIC FILES
# ----------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Якщо у тебе реально є папка /static в корені проекту — лишаємо.
# Якщо її нема — краще прибрати STATICFILES_DIRS.
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ----------------------
# MEDIA
# ----------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ----------------------
# AUTH
# ----------------------
LOGIN_URL = "/login/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ----------------------
# CORS / CSRF (ВАЖЛИВО для React кабінету)
# ----------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://alterhol.com.ua",
    "https://www.alterhol.com.ua",
]

CORS_ALLOW_CREDENTIALS = True

# Якщо колись буде робота з cookie/CSRF — краще додати trusted origins:
# Додайте ваш домен у список довірених
CSRF_TRUSTED_ORIGINS = [
    'https://alterhol.com.ua',
    'https://www.alterhol.com.ua',
    'https://energy-site.onrender.com' # адреса від рендер
]

# Переконайтеся, що сесії працюють через HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# ----------------------
# DRF + JWT
# ----------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ----------------------
# SECURITY (прод)
# ----------------------
# На проді можна ввімкнути, коли все ок:
# SECURE_SSL_REDIRECT = not DEBUG
# SESSION_COOKIE_SECURE = not DEBUG
# CSRF_COOKIE_SECURE = not DEBUG
