from rest_framework.viewsets import ModelViewSet

from clients.api.serializers import TenantSerializer
from clients.models import Client


class ClientsViewSet(ModelViewSet):
    def get_queryset(self):
        return Client.objects.all().order_by('-created_on')

    serializer_class = TenantSerializer
