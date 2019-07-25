from tenant_schemas.models import TenantMixin
from tenant_schemas.signals import post_schema_sync

from clients.cloud_tasks import track_model_tables


def hasura_auto_track_tables(sender, tenant, **kwargs):
    track_model_tables(tenant_id=tenant.id).execute()


post_schema_sync.connect(hasura_auto_track_tables, sender=TenantMixin)
