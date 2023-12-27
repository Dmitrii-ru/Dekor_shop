from celery import shared_task
from site_tools.utils.catalog.catalog_upload_v3 import transaction_upload_catalog

# celery -A core worker -B -Q site_tools
queue_app_name = 'site_tools'


@shared_task(queue=queue_app_name)
def create_update_catalog_task():
    transaction_upload_catalog()
