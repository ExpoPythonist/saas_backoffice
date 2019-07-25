import os

COMMON_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
]  # Apps we want on the public schema and other schemas too

SHARED_APPS = [
    'tenant_schemas',
    'clients',
    'hasura',
    *COMMON_APPS
]  # Just to make sure I remember what I'm doing in the next 2hrs, lol. These apps are synced to the public schema ONLY

TENANT_APPS = [
    *COMMON_APPS,

]  # These ones are synced to the individual schemas (ALL)

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

TENANT_MODEL = "clients.Client"

DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'

# PG_EXTRA_SEARCH_PATHS = ['extensions']

TENANT_LIMIT_SET_CALLS = True
PUBLIC_SCHEMA_URLCONF = 'django_hasura.urls_public'

MAIN_DOMAIN_URL = os.getenv('MAIN_DOMAIN_URL', 'localhost')

HASURA_URL = os.getenv('HASURA_URL', 'http://localhost:8080')
HASURA_SAAS_ACCESS_KEY = os.getenv('HASURA_SAAS_ACCESS_KEY', '')
