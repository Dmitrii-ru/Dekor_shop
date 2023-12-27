from celery import shared_task
from site_tools.utils.catalog.catalog_upload_v3 import transaction_upload_catalog

@shared_task
def create_update_catalog_task():
    transaction_upload_catalog()


