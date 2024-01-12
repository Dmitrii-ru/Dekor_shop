import os
from django.core.management import call_command
from django.db import transaction
from shop.models import Category, Group, Product
from site_tools.utils.catalog.dump_catalog.catalog_base_commend import CustomCatalogBaseCommand
from site_tools.utils.messages.create_db_massege import create_message_db


class Command(CustomCatalogBaseCommand):
    """
    Load on db dump file.
    Category, Group, Product
    """
    help = 'Load db dump file.\
    Category, Group, Product'

    def load_data_catalog(self):
        try:
            with transaction.atomic():
                call_command('loaddata', os.path.join(self.get_path_dump_dir(), self.dump_file_name))
                message = 'Резервная копия успешно обновила каталог'
                self.stdout.write(self.style.SUCCESS(message))
                create_message_db(message, notification=True)

        except Exception as e:
            message = f'Не возможно обновить каталог резервной копией: {str(e)}'
            self.stderr.write(self.style.ERROR(message))
            create_message_db(message)
            raise Exception(message)

    def handle(self, *args, **options):
        self.load_data_catalog()
