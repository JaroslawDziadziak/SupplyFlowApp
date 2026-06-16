"""
Django settings for config project.

"""
from pathlib import Path
# Importing decouple to read environment variables from .env file
from decouple import config

# Building paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Read from .env file using decouple - Never hardcode secrets!
SECRET_KEY = config('SECRET_KEY')

# Read from .env file using decouple
# config() converts string "True"/"False" to boolean
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',        # Django REST Framework for API endpoints
    'corsheaders',           # Adds CORS headers so Vue.js can call the API

    # My app
    'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration
# Changed from SQLite to PostgreSQL for production readiness
# PostgreSQL can handle multiple concurrent users and provides better data integrity

DATABASES = {
    'default': {
        # PostgreSQL database engine
        'ENGINE': 'django.db.backends.postgresql',
        
        # Database name - read from .env file
        # Matches the created database in PostgreSQL
        'NAME': config('DB_NAME'),
        
        # Database user - read from .env file
        'USER': config('DB_USER'),
        
        # Database password - read from .env file
        # NEVER hardcode passwords in code!
        'PASSWORD': config('DB_PASSWORD'),
        
        # Database host - where PostgreSQL server is running
        # Read from .env file (usually localhost)
        'HOST': config('DB_HOST'),
        
        # Database port - read from .env file
        # PostgreSQL default is 5432
        'PORT': config('DB_PORT'),
        
        # Connection timeout (in seconds)
        'CONN_MAX_AGE': 600,
    }
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Configuration
# Lists which frontend origins are allowed to call our API
# In production, replace this with your real frontend domain
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite dev server
]

# Django REST Framework Configuration
REST_FRAMEWORK = {
    # Default pagination - shows 10 items per page
    # This prevents returning millions of records at once
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # Authentication - JWT tokens instead of session cookies
    # This works across origins (Vue on :5173 → Django on :8000)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # Permissions - only authenticated users can access the API
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}