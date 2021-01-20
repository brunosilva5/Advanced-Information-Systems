from __future__ import absolute_import, unicode_literals
from .base import *
import os

env = os.environ.copy()

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


SECRET_KEY = env["SECRET_KEY"]

DEBUG = True

# Allow all host headers
ALLOWED_HOSTS = ["swotlab.herokuapp.com", "localhost", "127.0.0.1"]