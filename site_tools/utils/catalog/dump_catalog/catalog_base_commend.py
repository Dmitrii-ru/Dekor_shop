import os

from django.core.management.base import BaseCommand
from django.apps import apps


class CustomCatalogBaseCommand(BaseCommand):
    """
    Dump or load db
    Category, Group, Product
    """
    dump_file_name = 'dump.json'

    @staticmethod
    def get_path_dump_dir():
        """
        Get or make dir
        """
        app_path = apps.get_app_config('site_tools').path
        dump_dir = os.path.join(app_path, 'utils/catalog/dump_catalog/')
        if not os.path.exists(dump_dir):
            os.makedirs(dump_dir)
        return dump_dir

