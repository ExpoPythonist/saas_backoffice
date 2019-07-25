from django.db import models
from tenant_schemas.models import TenantMixin

from users.models import UserProxy


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    user = models.OneToOneField(UserProxy, null=True, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    # When true, the schema also gets deleted when the client account is deleted
    auto_drop_schema = True

    def __str__(self):
        return self.name
