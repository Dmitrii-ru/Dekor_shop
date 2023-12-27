from .models import Category, Group, Product
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Category)
def update_child_groups_is_active(sender, instance, **kwargs):
    if not instance.is_active:
        Group.objects.filter(category=instance).update(is_active=False)
        Product.objects.filter(group__in=instance.group.all()).update(is_active=False)


@receiver(pre_save, sender=Group)
def update_child_groups_is_active(sender, instance, **kwargs):
    if not instance.is_active:
        instance.product.all().update(is_active=False)

