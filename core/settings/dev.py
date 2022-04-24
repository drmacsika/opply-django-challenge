from .base import *

INSTALLED_APPS += [
    # Development packages
    "django_extensions",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
