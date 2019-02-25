# -*- coding: utf-8
DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "a secret key for testing"

DATABASES = {
    "default": {
        "NAME": "pytedjmi",
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "ATOMIC_REQUESTS": False,
        "AUTOCOMMIT": True,
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "tests"]

MIDDLEWARE = ()
