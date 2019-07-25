from django.db.models.signals import post_save, pre_delete

from clients.cloud_tasks import create_tenant_task
from users.models import UserProxy


def create_tenant(sender, instance, **kwargs):
    if kwargs.get('created') and instance.is_tenant:
        create_tenant_task(user_id=instance.id).execute()


def delete_tenant(sender, instance, **kwargs):
    if instance.is_tenant:
        from clients.models import Client
        Client.objects.filter(user=instance).delete()


post_save.connect(create_tenant, UserProxy)
pre_delete.connect(delete_tenant, UserProxy)
# We are using a pre delete signal and not letting it cascade because we need the schema also deleted
