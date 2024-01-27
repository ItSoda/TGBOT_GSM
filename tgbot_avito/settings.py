import os
from datetime import timedelta
from pathlib import Path

from decouple import Config, RepositoryEnv

docker = os.environ.get("DOCKER_CONTAINER")
test = os.environ.get("REDIS_TEST")
env_file = ".env"

if docker:
    env_file = "docker-compose.env"


config = Config(RepositoryEnv(env_file))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get("DEBUG", default=True)

DOMAIN_NAME = config.get("DOMAIN_NAME")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "tgbot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tgbot_avito.urls"

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main_format": {
            "format": "{asctime} - {levelname} - {module} - {filename} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "main_format",
        },
    },
    "loggers": {
        "main": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "tgbot_avito.wsgi.application"


# PARAMETRS FOR DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config.get("MYSQL_DATABASE", default="tgbot_avito"),
        "USER": config.get("MYSQL_ROOT_USER", default="root"),
        "PASSWORD": config.get("MYSQL_ROOT_PASSWORD", default="nik140406"),
        "HOST": config.get("MYSQL_HOST", default="localhost"),
        "PORT": config.get("MYSQL_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4"
        },
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
if docker:
    STATIC_ROOT = "static"
else:
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Base url to serve media files
MEDIA_URL = "/media/"
# Path where media is stored
MEDIA_ROOT = "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TELEGRAM BOT
TELEGRAM_BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN")

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://boar-still-alpaca.ngrok-free.app",
    "http://red-store.site",
    "https://red-store.site",
]
