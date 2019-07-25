import os

DJANGO_CLOUD_TASKS = {
    'project_location_name': 'projects/django-saas-237719/locations/us-central1',
    'task_handler_root_url': '/_tasks/'
}

# This setting allows you to debug your cloud tasks by running actual task handler function locally
# instead of sending them to the task queue. Default: False
DJANGO_CLOUD_TASKS_EXECUTE_LOCALLY = False

# If False, running `.execute()` on remote task will simply log the task data instead of adding it to
# the queue. Useful for debugging. Default: True
DJANGO_CLOUD_TASKS_BLOCK_REMOTE_TASKS = False

if not os.getenv('GAE_APPLICATION', None):
    DJANGO_CLOUD_TASKS_EXECUTE_LOCALLY = True
    DJANGO_CLOUD_TASKS_BLOCK_REMOTE_TASKS = True

DEFAULT_TASK_QUEUE = 'django-saas-queue'

DJANGO_CLOUD_TASKS_HANDLER_SECRET = 'xDsewdcvr3GydsUUislar2v8gwrim77x733'
