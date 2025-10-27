from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from decouple import config
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = [
    '127.0.0.1'
]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [
    "https://xplorecars.cc",
    "https://www.xplorecars.cc",
]


CSRF_TRUSTED_ORIGINS = [
    "https://admin.xplorecars.cc",
    "https://xplorecars.cc",
    "https://www.xplorecars.cc",
    "https://car-imports-production.up.railway.app",
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}
# Use Cloudinary for default file storage (media files)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}



JAZZMIN_SETTINGS = {
    "site_title": "Xplore Car Imports Admin",
    "site_header": "Xplore Admin",
    "site_brand": "Xplore Imports",
    "welcome_sign": "Welcome to Xplore Car Imports Dashboard",
    "site_logo": "images/logo.jpg",
    "custom_css": "css/admin-custom.css",
    "site_logo_classes": "brand-image",
    "copyright": "Xplore Car Imports © 2025",

    # Top menu (simple version)
    "topmenu_links": [
        {"name": "Home", "url": "/"},
        {"model": "auth.user"},
        {"app": "orders"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    # Colors
    "colors": {
        "accent": "#10B981",
        "accent_dark": "#047857",
        "primary": "#065F46",
        "secondary": "#6EE7B7",
        "link": "#059669",
        "hover": "#34D399",
        "bg": "#F9FAFB",
        "success": "#10B981",
        "warning": "#FBBF24",
        "danger": "#EF4444",
        "info": "#3B82F6",
    },

    # Buttons
    "button_classes": {
        "primary": "btn btn-success rounded-md px-4 py-2 shadow-md hover:shadow-lg",
        "secondary": "btn btn-outline-success rounded-md px-4 py-2",
        "warning": "btn btn-warning rounded-md px-4 py-2",
        "danger": "btn btn-danger rounded-md px-4 py-2",
        "info": "btn btn-info rounded-md px-4 py-2",
    },

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
}
