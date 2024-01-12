import openpyxl
from django.core.exceptions import ValidationError
from site_tools.utils.constants import const_columns


def get_header_catalog(catalog):
    """
    Get header df or raise.
    """
    header_catalog = None
    try:
        load_catalog = openpyxl.load_workbook(catalog, read_only=True, data_only=True)
        open_catalog = load_catalog.active

        for i, row in enumerate(open_catalog.iter_rows(values_only=True)):
            if const_columns.issubset(set(row)):
                header_catalog = i
                break

        if not header_catalog:
            raise ValidationError("В файле нет нужных колонок для загрузки каталога")
        return header_catalog

    except Exception as e:
        raise ValidationError(f"Ошибка при проверки файла {e}")
