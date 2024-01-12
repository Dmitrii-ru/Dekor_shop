import os
from django.core.management import call_command
from site_tools.utils.catalog.dump_catalog.catalog_base_commend import CustomCatalogBaseCommand
from site_tools.utils.messages.create_db_massege import create_message_db


class Command(CustomCatalogBaseCommand):

    help = 'Dump Category, Group, Product'

    def dump_data_catalog(self):
        path = os.path.join(self.get_path_dump_dir(), self.dump_file_name)
        try:
            with open(path, 'w') as file:
                call_command('dumpdata', 'shop.category', 'shop.group', 'shop.product', stdout=file)
            message = 'Резервная копия каталога успешно сохранена'
            create_message_db(message, notification=True)
            self.stdout.write(self.style.SUCCESS(message))

        except Exception as e:
            message = f'Не возможно создать резервную копию каталога сайта:: {str(e)}'
            self.stderr.write(self.style.ERROR(message))
            create_message_db(message)
            raise Exception(message)

    def handle(self, *args, **options):
        self.dump_data_catalog()
