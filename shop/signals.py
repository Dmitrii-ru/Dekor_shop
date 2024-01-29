from .models import Category, Group, Product, PromoProductGroup
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from celery import Celery
from .tasks import create_promo_end_date_task
from celery.result import AsyncResult


@receiver(pre_save, sender=Category)
def update_child_groups_is_active(sender, instance, **kwargs):
    if not instance.is_active:
        Group.objects.filter(category=instance).update(is_active=False)
        Product.objects.filter(group__in=instance.group.all()).update(is_active=False)


@receiver(pre_save, sender=Group)
def update_child_groups_is_active(sender, instance, **kwargs):
    if not instance.is_active:
        instance.product.all().update(is_active=False)


@receiver(post_save, sender=PromoProductGroup)
def promo_create_update(sender, instance, **kwargs):
    task_name = f'{PromoProductGroup._meta}_scheduled_{instance.id}'
    result = AsyncResult(task_name)
    result.revoke(terminate=True)
    create_promo_end_date_task.apply_async((instance.id,), eta=instance.end_date, task_id=task_name)

