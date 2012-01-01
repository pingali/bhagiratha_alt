import os,sys
from os.path import join, dirname, normpath
from django import templatetags 
from netifaces import interfaces, ifaddresses, AF_INET

SECRET_KEY = '=hf03e+08xlolbb$!-s01m-n_4xn*5mdsd!pm@$+ms!pe08f-7'

##############################################################
# Helper functions 
##############################################################

# Find local ip address
def get_host_type(): 

    # use whatever complicated logic
    addresses = [i['addr'] for i in ifaddresses('eth0').setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    if "192.168" in addresses[0]: 
        return "development" 
    elif "10." in addresses[0]: 
        return "production" 
    else: 
        raise Exception("Cannot determine execution mode for host '%s'.  Please check DEVELOPMENT_HOST and PRODUCTION_HOST in settings_local.py." % node())

def findpath(path):
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(parent_dir,path))

##############################################################
# Adjust path
##############################################################

# For oauth2resource and oauth2 app 
sys.path.insert(0, findpath(".."))


# Shared settings 
ADMINS = ()
MANAGERS = ADMINS

##############################################################
# Recaptcha 
##############################################################
RECAPTCHA_PUBLIC_KEY="6LefI8sSAAAAAPW4I8Bs0Qb5DZToQLe_Q6Uq-zaH"
RECAPTCHA_PRIVATE_KEY="6LefI8sSAAAAAL5jzNKsivcBWJG-Fxwak8pRLPxb"
RECAPTCHA_USE_SSL=False


##############################################################
# Adjust path
##############################################################
TIME_ZONE = 'Asia/Kolkata'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
LOGIN_URL = "/account/login"
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/static/admin/'

##############################################################
# Cookie management 
##############################################################

#SESSION_COOKIE_DOMAIN=DEPLOYMENT_SERVER
SESSION_COOKIE_NAME="bhagirathsite"
CSRF_COOKIE_NAME="bhagirathcsrf" 

##############################################################
# Static Files 
##############################################################

STATICFILES_DIRS = (findpath('static'),)
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#############################################################
# Generic authentication 
##############################################################
AUTH_PROFILE_MODULE = "account.UserProfile"
AUTHENTICATION_BACKENDS = (     
    'django.contrib.auth.backends.ModelBackend',
    )

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

##############################################################
# Set up the aadhaar configuration
##############################################################

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'bhagirath.urls'

##############################################################
# Manage template paths
##############################################################
TEMPLATE_DIRS = (
    findpath('templates'),
    )
# => Hack to include the template tags
for mod in ['bhagirath']: 
    templatetags.__path__.extend(__import__(mod + '.templatetags', {},{}, ['']).__path__)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

##############################################################
# Generic authentication 
##############################################################
#AUTH_PROFILE_MODULE = "account.UserProfile"
AUTHENTICATION_BACKENDS = (     
    'django.contrib.auth.backends.ModelBackend',
    )

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

##############################################################
# Complete list of apps 
##############################################################
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'uni_form',
    'captcha',
    'bhagirath.apps.base',
    'bhagirath.apps.account',
    'bhagirath.apps.documents',
    'bhagirath.apps.microtasks',
    'south',
    )
