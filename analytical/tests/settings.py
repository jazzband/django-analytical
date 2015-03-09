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
    'analytical',
]

SECRET_KEY = 'testing'

MIDDLEWARE_CLASSES=('django.middleware.common.CommonMiddleware',
                    'django.middleware.csrf.CsrfViewMiddleware'),
