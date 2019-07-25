import os
import logging

from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.http import JsonResponse, Http404
from rest_framework import status
from tenant_schemas.middleware import DefaultTenantMiddleware
from tenant_schemas.utils import get_tenant_model, get_public_schema_name

logger = logging.getLogger(__name__)


# These hostnames will be converted to "localhost"
allowed_hosts = ['127.0.0.1', '10.0.3.2', '35.238.147.161', '.senseandserve.com', 'orghub.senseandserve.com']


class SAASMiddleware(DefaultTenantMiddleware):
    """
    In the case of authentication from hasura where you need to specifically declare only one endpoint for auth,
    we specify the sub-domain through the request header 'X-HASURA-TARGET-SCHEMA',
    for example X-HASURA-TARGET-SCHEMA=public
    """

    def process_hasura_webhook_auth(self, request):
        meta = request.META
        schema_from_header = meta.get('X-HASURA-TARGET-SCHEMA', meta.get('HTTP_X_HASURA_TARGET_SCHEMA',
                                                                         get_public_schema_name()))
        if not schema_from_header:
            return JsonResponse(data='You need to set header \'X-HASURA-TARGET-SCHEMA\' to the target sub-domain '
                                     'name', status=status.HTTP_401_UNAUTHORIZED, safe=False)
        tenant = get_tenant_model().objects.get(schema_name=schema_from_header)
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()

    def process_request(self, request):
        super(SAASMiddleware, self).process_request(request)
        webhook_url = os.getenv('HASURA_SAAS_AUTH_WEBHOOK', '/hasura/webhook/auth/')
        if webhook_url and webhook_url in request.build_absolute_uri():
            return self.process_hasura_webhook_auth(request)

    def get_tenant(self, model, hostname, request):
        try:
            """In case we are running in a docker container within same machine"""
            hostname = hostname.replace('host.docker.internal', 'localhost')
            print('\n\n\nMy Hostname is \n\n\n', hostname, '\n\n\n')
            if any(allowed_host in hostname for allowed_host in allowed_hosts):
                hostname = 'localhost'

            return super(DefaultTenantMiddleware, self).get_tenant(model, hostname, request)
        except model.DoesNotExist:
            raise Http404('Sub-domain requested does not exist')
