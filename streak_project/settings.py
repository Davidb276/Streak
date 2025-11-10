# streak_project/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-streak-key'  # cambia esto en producción
DEBUG = True
ALLOWED_HOSTS = []

# Aplicaciones principales
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    
    # Apps del proyecto
    'users',
    'vacancies',
    'challenges',
    'ai_module',
    'notifications',
    "widget_tweaks",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'streak_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Plantillas globales
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

WSGI_APPLICATION = 'streak_project.wsgi.application'

# Base de datos (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Autenticación
AUTH_USER_MODEL = 'users.User'

# URLs de login/logout
LOGIN_REDIRECT_URL = "home"   # Página a la que va tras iniciar sesión
LOGOUT_REDIRECT_URL = "home"  # Página a la que va tras cerrar sesión
LOGIN_URL = "login"            # Para usar @login_required

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# 📬 Configuración de envío de correos con SendGrid
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT = True

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# ⏰ Tareas programadas (cron jobs)
CRONJOBS = [
    # Ejecutar cada día a las 9:00 a.m.
    ('0 9 * * *', 'notifications.email_service.enviar_recordatorios')
]

