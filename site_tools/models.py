from django.db import models

from .utils.catalog.constants import create_status_catalog
from .utils.custom_storage import DocumentStorage

from .utils.catalog.get_header_catalog import get_header_catalog
from django.utils import timezone


def get_time_upload(data):
    return timezone.localtime(data).strftime("%Y-%m-%d %H:%M:%S")


# Create your models here.
class SingletonModel(models.Model):
    """
    ABS Single model
    Replaces object
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            if Catalog.objects.filter(pk=1):
                Catalog.objects.get(pk=1).delete()
            self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Catalog(SingletonModel):
    catalog = models.FileField(
        'Каталог',
        upload_to='catalog',
        storage=DocumentStorage(),
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField('Статус', default=create_status_catalog(1))
    header_df = models.IntegerField('Шапка каталога (строка)', null=True, blank=True)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталог'

    def __str__(self):
        return f'Статус: {self.status} | Дата загрузки каталога: ' \
               f'{get_time_upload(self.uploaded_at)} '

    def save(self, *args, **kwargs):
        if not self.uploaded_at:
            self.uploaded_at = timezone.now()
            self.header_df = get_header_catalog(self.catalog)
        if self.status == create_status_catalog(1):
            self.status = create_status_catalog(2)
            self.save()
            from .tasks import create_update_catalog_task
            create_update_catalog_task.delay()
        super().save(*args, **kwargs)


class ReportCatalog(models.Model):
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
    report = models.FileField(
        'Отчет каталога',
        blank=True,
        max_length=1000,
        storage=DocumentStorage(),
        upload_to='catalog_reports',
    )

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчет загрузки каталога'

    def __str__(self):
        return f'Отчет загрузки каталога {get_time_upload(self.uploaded_at)}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ErrorMessage(models.Model):
    message = models.TextField('Сообщение')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{get_time_upload(self.uploaded_at)} - {self.message[20:]}'
