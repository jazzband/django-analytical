"""
django-analytical testing settings.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'analytical',
]

SECRET_KEY = 'testing'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)
