"""
Project related custom settings
"""
import os
import warnings

from dotenv import load_dotenv
from .django import *
from django.core.exceptions import ImproperlyConfigured

# set env variables as os env variables
load_dotenv()


def get_env_value(env_variable, optional=False):
    """
    get env variable from env file
    """
    try:
        return os.environ[env_variable]
    except KeyError:
        message = f"Env Variable {env_variable} not set!"
        if not optional:
            raise ImproperlyConfigured(message)
        warnings.warn(message)
        return None


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_value("POSTGRES_DB"),
        "USER": get_env_value("POSTGRES_USER"),
        "PASSWORD": get_env_value("POSTGRES_PASSWORD"),
        "HOST": get_env_value("DATABASE_HOST"),
        "PORT": get_env_value("DATABASE_PORT")
    }
}


# ORM APPS
INSTALLED_APPS += [
    "survey",
    "django.contrib.sites"
]
SITE_ID = 1

# Custom settings
DEFAULT_PAGE_SIZE = 10
CSRF_COOKIE_SECURE = False

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
