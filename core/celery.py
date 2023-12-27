import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def is_active_tasks():
    inspector = app.control.inspect()
    active_tasks = inspector.active()
    print(active_tasks)
