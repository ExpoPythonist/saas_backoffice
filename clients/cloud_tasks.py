import random
import string
import logging

from django.apps import apps
from django.conf import settings
from django_cloud_tasks import task, views
from tenant_schemas.utils import tenant_context

from clients.models import Client
from clients.utils import generate_client_url
from hasura.api.schema.tables import track
from users.models import User

logger = logging.getLogger(__name__)


@task(queue=settings.DEFAULT_TASK_QUEUE)
def create_tenant_task(request, user_id):
    user = User.objects.get(pk=user_id)
    from clients.models import Client

    logger.info('Generating tenant account for {}'.format(user.username))

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    try:
        tenant_sub_domain = user.username or user.first_name or user.last_name or id_generator()
        tenant = Client(name=user.get_full_name(), user=user,
                        domain_url=generate_client_url(tenant_sub_domain),
                        paid_until=None, on_trial=True, schema_name=tenant_sub_domain)
        tenant.save()
    except Exception as e:
        logger.error('Error generating tenant for {}'.format(user.username))
        logger.error(str(e))

    logger.info('Tenant generation complete for {}'.format(user.username))


@task(queue=settings.DEFAULT_TASK_QUEUE)
def track_model_tables(request, tenant_id):
    tenant = Client.objects.get(pk=tenant_id)
    apps_to_track_tables = settings.TENANT_APPS
    for app in apps_to_track_tables:
        models = apps.all_models[app]
        for key in models.keys():
            Model = models[key]
            if hasattr(Model, 'Hasura') and Model.Hasura.track:
                track(tenant.schema_name, Model._meta.db_table)
    # Replicates the user login to their schema
    replicate_user_to_own_domain(tenant_id=tenant.id).execute()


@task(queue=settings.DEFAULT_TASK_QUEUE)
def replicate_user_to_own_domain(request, tenant_id):
    tenant = Client.objects.get(pk=tenant_id)
    user = tenant.user
    with tenant_context(tenant):
        user.id = None
        user.is_tenant = False
        user.is_staff = True
        user.is_superuser = True
        user.save()
