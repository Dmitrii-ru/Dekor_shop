import os
from django.core.management import call_command
from django.apps import apps
from django.db import transaction

from shop.models import Category, Group, Product
from site_tools.utils.error_logs.create_db_massege import create_message_db

dump_file_name = 'dump.json'

def get_path_dump_dir():
    app_path = apps.get_app_config('site_tools').path
    dump_dir = os.path.join(app_path, 'utils/catalog/dump_catalog/')
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    return dump_dir


def dump_data_catalog():

    path = os.path.join(get_path_dump_dir(), dump_file_name)
    try:
        with transaction.atomic():
            Category.objects.all()
            Group.objects.all()
            Product.objects.all()
            with open(path, 'w') as file:
                call_command('dumpdata', 'shop.category', 'shop.group', 'shop.product', stdout=file)
            print('Успешный dump каталога')
    except Exception as e:
        er = f'Не возможно создать резервную копию каталога сайта: {str(e)}'
        create_message_db(er)
        print(er)
        raise Exception(er)


def load_date_catalog():
    try:
        with transaction.atomic():
            Category.objects.all()
            Group.objects.all()
            Product.objects.all()
            call_command('loaddata', get_path_dump_dir() + dump_file_name)
            mess = 'Каталог успешно восстановлен'
            create_message_db(mess, notification=True)
    except Exception as e:
        mess = f'Ошибка восстановления каталога -> {str(e)}'
        create_message_db(mess)
        raise Exception(mess)


