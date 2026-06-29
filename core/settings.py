from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from decouple import config
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# CORE SECURITY
# =====================
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DEBUG', default='False') == 'True'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Automatically include Railway's internal URL if present
RAILWAY_STATIC_URL = os.getenv('RAILWAY_STATIC_URL', '')
if RAILWAY_STATIC_URL:
    ALLOWED_HOSTS.append(RAILWAY_STATIC_URL)

# =====================
# INSTALLED APPS
# =====================
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
    'django_ckeditor_5',
    'api',
]

# =====================
# MIDDLEWARE
# =====================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# =====================
# DATABASE
# =====================
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}

# =====================
# PASSWORD VALIDATION
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =====================
# LOCALISATION
# =====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# =====================
# STATIC FILES
# =====================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====================
# CORS & CSRF
# =====================
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config(
        'CORS_ALLOWED_ORIGINS',
        default='https://xplorecars.cc,https://www.xplorecars.cc,http://localhost:8080'
    ).split(',')
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config(
        'CSRF_TRUSTED_ORIGINS',
        default='https://xplorecars.cc,https://www.xplorecars.cc,http://localhost:8080'
    ).split(',')
]

# =====================
# CLOUDINARY
# =====================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# =====================
# REST FRAMEWORK
# =====================
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


CKEDITOR_5_CONFIGS = {
    # `django_ckeditor_5` expects config sets keyed by name. The widget
    # defaults to the "default" config name, so provide one here.
    'default': {
        'toolbar': [
            'heading',
            '|',
            'bold',
            'italic',
            'underline',
            'link',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'insertTable',
            'imageUpload',
            '|',
            'undo',
            'redo',
        ]
    }
}

# =====================
# JAZZMIN ADMIN THEME
# =====================
JAZZMIN_SETTINGS = {
    'site_title': config('JAZZMIN_SITE_TITLE', default='Xplore Car Imports Admin'),
    'site_header': config('JAZZMIN_SITE_HEADER', default='Xplore Admin'),
    'site_brand': config('JAZZMIN_SITE_BRAND', default='Xplore Imports'),
    'welcome_sign': 'Welcome to Xplore Car Imports Dashboard',
    'site_logo': 'images/logo.jpg',
    'custom_css': 'css/admin-custom.css',
    'site_logo_classes': 'brand-image',
    'copyright': 'Xplore Car Imports © 2025',

    'topmenu_links': [
        {'name': 'Home', 'url': '/'},
        {'model': 'auth.user'},
    ],

    'show_sidebar': True,
    'navigation_expanded': True,

    'colors': {
        'accent': '#10B981',
        'accent_dark': '#047857',
        'primary': '#065F46',
        'secondary': '#6EE7B7',
        'link': '#059669',
        'hover': '#34D399',
        'bg': '#F9FAFB',
        'success': '#10B981',
        'warning': '#FBBF24',
        'danger': '#EF4444',
        'info': '#3B82F6',
    },

    'button_classes': {
        'primary': 'btn btn-success rounded-md px-4 py-2 shadow-md hover:shadow-lg',
        'secondary': 'btn btn-outline-success rounded-md px-4 py-2',
        'warning': 'btn btn-warning rounded-md px-4 py-2',
        'danger': 'btn btn-danger rounded-md px-4 py-2',
        'info': 'btn btn-info rounded-md px-4 py-2',
    },

    'changeform_format': 'horizontal_tabs',
}