from celery import shared_task

# celery -A core worker -B -Q shop

queue_app_name = 'shop'


@shared_task(queue=queue_app_name)
def create_promo_end_date_task(obj_id):
    print(obj_id, '# celery -A core worker -B -Q shop')
