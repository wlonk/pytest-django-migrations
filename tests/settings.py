# -*- coding: utf-8
import dj_database_url


DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "a secret key for testing"

DATABASES = {"default": dj_database_url.config(default="postgres:///pytedjmi")}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = ["django.contrib.auth", "django.contrib.contenttypes", "tests"]

MIDDLEWARE = ()
