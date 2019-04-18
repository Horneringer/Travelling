"""
Django settings for travel project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# конструкция позволяет определить переменные из переменных окружений, которые позже определяются на Heroku
# вытягиваем из окружения и передаём в переменную для настройки БД
DB_NAME = os.environ.get('DB_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# поднимаем расположение BASE_DIR на один уровень вверх(так как раньше файл settings был на уровне travel,
# а тeперь он находится в папке settings и представлен ввиде 2х файлов
# production и local); это можно сделать добавлением ещё одного "os.path.dirname"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'iv10)rxux2l*buikioy2^pzyrtchgt0je^_4vhk%r-r#4)l+y0'

# изначально в версии для продакшна не будет ключа(None);
# для развёртки проекта необходимо указать ключ единожды, а птом он будет прописан в переменных окружениях Heroku
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['travelling-django.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities',
    'trains',
    'routes',
]

# подключаем whitenoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'travel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'travel.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# меняем запись для работы с postgreSQL, так как sqlite поддерживает только одно подключение и не подходит для prod версии
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # переменные окружения, которые предоставит Heroku; после их записи сюда, можно будет использовать предоставленную БД
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        # стандартный порт для postgres
        'PORT': '5432'
    }
}

# на сайте https://pypi.org/project/python-dotenv/0.1.0/ есть библиотека,
# с помощью которой можно легко скрывать необходимые данные от посторонних при развертке проета
import dj_database_url

db = dj_database_url.config()
DATABASES['default'].update(db)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# переменная для работы со статикой
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
