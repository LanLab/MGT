# CHANGE SETTINGS FOR YOUR PROJECT HERE!
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YourSecretKey.......!!!!!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', '[::1]', '*']


# Application definition

INSTALLED_APPS = [
    'django_tables2',
    'Home',
    'Salmonella',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'rest_framework',
	'django_registration',
	'django_countries',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Mgt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Home/templates/'), os.path.join(BASE_DIR, 'Home/templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				'Mgt.context_processors.root_url',
            ],
        },
    },
]

MY_URL = "http://127.0.0.1:8000"
WSGI_APPLICATION = 'Mgt.wsgi.application'



DATABASE_ROUTERS = ['Mgt.router.GenericRouter']
APPS_DATABASE_MAPPING = {'Salmonella': 'salmonella',
                         'Vibrio': 'vibrio'}
# provide your mapping here!

# update this for main page display;
# DATABASE_ORGNAME_MAPPING = {
#    'Salmonella': 'Salmonella enterica', 'Vibrio': "Vibrio Cholerae"}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '0.0.0.0',
        'PORT': '5432',
        'USER': 'dbUserName',
        'PASSWORD': 'securePassword',
        'NAME': 'default',
    },
    'salmonella': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '0.0.0.0',
        'PORT': '5432',
        'USER': 'dbUserName',
        'PASSWORD': 'securePassword',
        'NAME': 'salmonella',
    },
}

# can add additional databases as
#     'vibrio': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'HOST': '0.0.0.0',
#        'PORT': '5432',
#        'USER': 'dbUserName',
#        'PASSWORD': 'securePassword',
#        'NAME': 'vibrio',
#    },

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

# or HMAC activation workflow. Change to your required settings
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window;
INCLUDE_REGISTER_URL = True
REGISTRATION_OPEN = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = 'yourEmailHostUserName'
EMAIL_HOST_PASSWORD = 'yourEmailHostPassword'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'yourEmailNotificatonServer@address'
LOGIN_REDIRECT_URL = '/'



SUBDIR_REFERENCES = 'location/to/References/'
SUBDIR_ALLELES = 'location/to/Alleles/'
MEDIA_ROOT = "location/to/Uploads/"



# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_FORMAT = 'Y-m-d'


# your static file's folder location.
STATIC_URL = '/static/'
STATIC_ROOT = 'Static/'
