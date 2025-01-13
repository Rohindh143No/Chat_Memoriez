import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
  # Replace with a proper method to set it securely in production
SECRET_KEY = 'django-insecure-^q1n92h*=4fl5l+iu)gqatfa5s@%n_u4#r^)fve%8$i&l+slyn'

# Debug Mode (Should be False in production)
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = []  # Add all allowed domains for production here

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',  # Your chat app
    'file_display',  # Your file display app (if any)
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'memoriez.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# WSGI application
WSGI_APPLICATION = 'memoriez.wsgi.application'

# Media configuration (File uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Use absolute path for PythonAnywhere

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # This is for local development; for production, STATIC_ROOT will be used
#STATIC_ROOT = BASE_DIR / 'staticfiles'  # Collect static files here in production


# Location of static files in development (for non-app static files like stylesheets, images, etc.)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'memoriez'),  # Your project's static files directory
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database configuration (SQLite in this case)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files storage (for production)

# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Uncomment and configure this for production if needed.
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Uncomment and configure this for production if needed.
#STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

