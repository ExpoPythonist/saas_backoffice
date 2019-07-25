from django.conf import settings


def generate_client_url(subdomain):
    if settings.IS_GAE:
        return f'{subdomain}-dot-{settings.MAIN_DOMAIN_URL}'
    return f'{subdomain}.{settings.MAIN_DOMAIN_URL}'
