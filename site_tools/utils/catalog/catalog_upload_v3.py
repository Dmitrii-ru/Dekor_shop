import os
from typing import Any
import pandas as pd
from django.db import transaction
from shop.models import Category, Group, Product
from site_tools.models import Catalog
import zipfile
import xml.etree.ElementTree as ET
from site_tools.utils.catalog.object_create import ObjectCreate
from site_tools.utils.catalog.object_update import ObjectUpdate
from site_tools.utils.report.report_create import create_report
from site_tools.utils.constants import report_columns_dict, report_message, stop_list_product
from site_tools.utils.messages.create_db_massege import create_message_db
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command


class TempCategoryUpdate(ObjectUpdate):
    model_django = Category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TempCategoryCreate(ObjectCreate):
    model_django = Category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self):
        super(TempCategoryCreate, self).create()
        obj = super().create()
        self.model_django.objects.bulk_create([obj, ])
        return obj


class TempGroupUpdate(ObjectUpdate):
    model_django = Group

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TempGroupCreate(ObjectCreate):
    model_django = Group

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self):
        super(TempGroupCreate, self).create()
        obj = super().create()
        self.model_django.objects.bulk_create([obj, ])
        return obj


class TempProductUpdate(ObjectUpdate):
    model_django = Product

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class TempProductCreate(ObjectCreate):
    model_django = Product

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.sv_site_name = None

    def create(self):
        super(TempProductCreate, self).create()
        obj = super().create()
        self.models_dict['to_create'].append(obj)
        return obj


class CatalogUploader:
    """
    - Get levels excel file
    - Validate data
    - Update fields
    - Create objects
    - Building objects models connections
    - Data collections at report
    """

    models_list = [Category, Group, Product]

    def __init__(self, catalog_db):
        self.catalog_db = catalog_db
        self.models_dict = {}
        self.list_models = CatalogUploader.models_list
        self.report = self.Report(self.list_models)

    class Report:

        def __init__(self, list_models):
            self.rep = {m._meta.verbose_name_plural: {} for m in list_models}
            self.keys_columns = list(
                report_columns_dict.values())

        def new_record(self, model_plural: str, column: str, value: Any, obj: Any) -> None:
            column = report_columns_dict[column]
            value = report_message[value]
            if obj.art not in self.rep[model_plural]:
                self.rep[model_plural][obj.art] = {
                    'report': {'Название': obj.name}
                }
            self.rep[model_plural][obj.art]['report'][column] = value

    def create_dict_models(self):
        """
        Creating dictionaries to store models data
        """
        for model in self.list_models:
            model_all = model.objects.all()
            self.models_dict[f'{model}'] = {
                'art_obj_dict': {obj.art: obj for obj in model_all},
                'to_update': {},
                'to_create': [],
                'art_list': [],
                'name_list': {obj.name: obj for obj in model_all},
                'site_name_list': {obj.site_name: obj for obj in model_all}
            }

    def open_df(self):
        """
        Open df
        """
        excel_data_df = pd.read_excel(self.catalog_db.catalog, header=self.catalog_db.header_df, engine='openpyxl')
        import numpy as np
        excel_data_df = excel_data_df.replace({np.nan: None})
        return excel_data_df, self.catalog_db.header_df

    def temp_catalog_parser(self):
        """
        Parsing catalog
        Create temp objects
        Start update_create db
        """
        with zipfile.ZipFile(os.path.abspath("Тест каталог.xlsx"), 'r') as zip_ref:
            with zip_ref.open('xl/worksheets/sheet1.xml') as sheet_file:
                sheet_tree = ET.parse(sheet_file)
                sheet_root = sheet_tree.getroot()
                schema_rows = sheet_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')
                excel_data_df, header = self.open_df()
                category = None
                group = None
                self.create_dict_models()

                for schema_row in schema_rows[header + 1:]:
                    outline_level = int(schema_row.get('outlineLevel', 0))
                    row_number = int(schema_row.get('r')) - header - 2
                    row = excel_data_df.iloc[row_number]
                    if outline_level == 1:
                        art = str(row['Номенклатура.Код'])
                        category_object = self.models_dict[f'{Category}']['art_obj_dict'].get(art, None)
                        temp_category_dict = dict(
                            name=row['Номенклатура'],
                            site_name=row['Номенклатура'],
                            art=art,
                            models_dict=self.models_dict[f'{Category}'],
                            report=self.report,
                            update_obj=category_object
                        )

                        if category_object:
                            category = TempCategoryUpdate(**temp_category_dict).update()
                        else:
                            category = TempCategoryCreate(**temp_category_dict).create()

                    elif outline_level == 2:
                        art = str(row['Номенклатура.Код'])
                        group_object = self.models_dict[f'{Group}']['art_obj_dict'].get(art, None)

                        temp_group_dict = dict(
                            name=row['Номенклатура'],
                            site_name=row['Номенклатура'],
                            art=art,
                            category=category,
                            models_dict=self.models_dict[f'{Group}'],
                            report=self.report,
                            update_obj=group_object
                        )

                        if group_object:
                            group = TempGroupUpdate(**temp_group_dict).update()
                        else:
                            group = TempGroupCreate(**temp_group_dict).create()

                    elif outline_level == 3:

                        if not any(row['Номенклатура'].strip().startswith(stop) for stop in stop_list_product):
                            art = str(row['Номенклатура.Код'])
                            product_object = self.models_dict[f'{Product}']['art_obj_dict'].get(art, None)

                            temp_product_dict = dict(
                                name=row['Номенклатура'],
                                site_name=row['Наименование полное'],
                                art=art,
                                price=row["Розничная цена"],
                                unit=row['Ед. изм.'],
                                stock=row['Остаток на складе'],
                                group=group,
                                models_dict=self.models_dict[f'{Product}'],
                                report=self.report,
                                update_obj=product_object
                            )

                            if product_object:
                                TempProductUpdate(**temp_product_dict).update()
                            else:
                                print(row['Номенклатура.Код'], len(str(row['Номенклатура.Код'])))
                                print(product_object)
                                TempProductCreate(**temp_product_dict).create()
        self.bulk_update_create_objects()
        return self.report

    def search_no_actual_objects(self, model) -> None:
        """
        Looking objs that are not in downloaded catalog, but are in db
        Update field is_active=False
        """

        list_objects = self.models_dict[f'{model}']['art_list']

        if list_objects:
            objs = model.objects.all().exclude(art__in=list_objects)
            if objs:
                objs.update(is_active=False)
                for obj in objs:
                    self.report.new_record(model._meta.verbose_name_plural, 'is_actual_false', 5, obj)

    def bulk_update_create_objects(self):
        """
        Create Update Is_active=False DB
        """

        for model in self.list_models:
            self.search_no_actual_objects(model)
            to_update = self.models_dict[f'{model}']['to_update']
            if to_update:
                for fields_set, values in to_update.items():
                    model.objects.bulk_update(
                        values,
                        fields=list(fields_set),
                        batch_size=100
                    )
        products_to_create = self.models_dict[f'{Product}'].get('to_create', None)
        if products_to_create:
            Product.objects.bulk_create(products_to_create, batch_size=100)


def transaction_upload_catalog():
    """
    Manager of the store assortment updating process
    - Transaction update db models
    - Create Report
    - Delete catalog
    """
    catalog = None
    report = None
    success_flag = True
    error_message = None

    with transaction.atomic():
        try:
            catalog = Catalog.objects.get(pk=1)
        except ObjectDoesNotExist as e:
            error_message = f'Каталог не обнаружен. {str(e)}'
            create_message_db(error_message)
            success_flag = False

        call_command('catalog_dump')

        try:
            sp = transaction.savepoint()
            Category.objects.select_for_update().all()
            Group.objects.select_for_update().all()
            Product.objects.select_for_update().all()
            report = CatalogUploader(catalog).temp_catalog_parser()
        except ValueError as e:
            transaction.savepoint_rollback(sp)
            error_message = f'Каталог не загружен.{str(e)}'
            create_message_db(error_message)
            success_flag = False

    if success_flag:
        try:
            catalog.status = 'Готовлю отчет'
            catalog.save()
            create_report(report)

        except Exception as e:
            create_message_db(f'Отчет по каталогу не создан.{str(e)}')

        finally:
            catalog.delete()
            create_message_db(
                "Каталог успешно обновлен и файл удален, подготовлен отчет и резервная копия.",
                notification=True
            )
    else:
        catalog.status = error_message
        catalog.save()
