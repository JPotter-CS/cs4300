import os
from pathlib import Path


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bookings',
]

#Set base directory to path to make it easy for referencing
BASE_DIR = Path(__file__).resolve().parent.parent

# These are used to help process requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#Pretty much tells django where to look for url patterns
ROOT_URLCONF = "movie_theater_booking.urls"

# Set debug to true to make it easier to figure out what I did wrong while testing. Research showed to ensure that it
# is set to false before running in production
DEBUG = True

SECRET_KEY = '5-g%!t^z56mnj(o!$o6%n-k%2%^--h&$l^qh9k1841!(v0!e6#'

# This ensures it can accept requests from any address
ALLOWED_HOSTS = ['*']

# Configurations for REST framework
REST_FRAMEWORK = {

    # This ensures that API access requires authentication
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Adds support for session and basic authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    # Esnures it returns results in pages
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # only allow 20 results per page
    'PAGE_SIZE': 20
}

#HTML configuration
TEMPLATES = [
    {
        # Backend uses django templates
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # Ensures it loads template from app
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Setting the database to use sqlite3 and where to make the db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Whitelisting the devedu domain for the app. Before this I was having major issues with loading URLs and API in the app
CSRF_TRUSTED_ORIGINS = [
    'https://app-jpotter4-20.devedu.io',
]

# We are using static files for web app. 
STATIC_URL = '/static/'
