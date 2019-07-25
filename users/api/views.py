from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from tenant_schemas.utils import get_public_schema_name

from clients.models import Client
from users.api.serializers import UserSerializer
from users.models import UserProxy as User


class UserViewSet(ModelViewSet):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return User.objects.all()

    serializer_class = UserSerializer

    @action(methods=['GET'], detail=False, url_path='profile', permission_classes=[IsAuthenticated])
    def profile(self, request, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        return Response(self.serializer_class(user).data, status=200)

    @action(methods=['GET'], detail=False, url_path='subdomain-by-host', permission_classes=[AllowAny])
    def subdomain_by_host(self, request, **kwargs):
        """Carries URL param 'hostname' for a GET request"""
        hostname = self.request.query_params.get('hostname', '')
        domain = self.request.query_params.get('domain', '')
        match = hostname.replace(domain, settings.MAIN_DOMAIN_URL)
        subdomain = get_object_or_404(Client, domain_url=match)
        domain_url = subdomain.domain_url
        schema_name = subdomain.schema_name
        if schema_name == get_public_schema_name():
            return Response({'domain_url': domain_url.replace(schema_name + '.', ''),
                             'subdomain': schema_name.replace(schema_name, '')}, status=200)
        return Response({'domain_url': domain_url, 'subdomain': schema_name}, status=200)

    @action(methods=['GET'], detail=False, url_path='host-by-subdomain', permission_classes=[AllowAny])
    def host_by_subdomain(self, request, **kwargs):
        """Carries URL param 'subdomain'"""
        subdomain = self.request.query_params.get('subdomain', get_public_schema_name())
        if not subdomain:
            subdomain = get_public_schema_name()
        subdomain = get_object_or_404(Client, schema_name=subdomain)
        domain_url = subdomain.domain_url
        if not settings.IS_GAE and request.META.get('SERVER_PORT') and str(request.META.get('SERVER_PORT')) not in \
                ['80', '443']:
            domain_url += ':' + request.META.get('SERVER_PORT')
        if request.is_secure and 'localhost' not in request.get_host() and '127.0.0.1' not in request.get_host():
            domain_url = 'https://' + domain_url
        else:
            domain_url = 'http://' + domain_url
        return Response({'domain_url': domain_url})
