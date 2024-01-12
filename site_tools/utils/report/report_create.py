import os
from datetime import timezone
import pandas as pd
import openpyxl
from django.core.exceptions import ValidationError
from core import settings

from django.utils import timezone
from site_tools.models import ReportCatalog
from datetime import datetime
from core.settings import TIME_ZONE
import datetime
from pytz import timezone


def get_time_now():
    """
    Get local time now.
    """
    tz = timezone(TIME_ZONE)
    current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def create_report(report):
    """
    Create report, each model has it on own page, sorted columns, size cell.
    Save report.
    """
    try:
        list_col = ["Номенклатура.Код", "Название"] + report.keys_columns

        report_directory = os.path.join(settings.DOCUMENT_ROOT, 'catalog_reports')
        os.makedirs(report_directory, exist_ok=True)
        name_repost = f'Отчет загрузки каталога-{get_time_now()}.xlsx'
        report_path = os.path.join(report_directory, name_repost)

        with pd.ExcelWriter(report_path, engine='xlsxwriter') as writer:
            for model, model_values in report.rep.items():
                columns = set()
                rows = []
                for art, values in model_values.items():
                    report = values['report']
                    report["Номенклатура.Код"] = art
                    columns.update(report.keys())
                    rows.append(report)

                df = pd.DataFrame(
                    rows,
                    columns=list(sorted(columns, key=lambda x: list_col.index(x) if x in list_col else float('inf')))
                )
                df = df.fillna('')
                df.to_excel(writer, sheet_name=model, index=False)
                for idx, col_name in enumerate(columns):
                    max_len = max(df[col_name].astype(str).apply(len).max(), len(col_name))
                    writer.sheets[model].set_column(idx, idx, max_len + 2)

        path_report = os.path.relpath(report_path, settings.DOCUMENT_ROOT)
        r = ReportCatalog.objects.create(report=path_report, is_active_dump=True)
        ReportCatalog.objects.filter(is_active_dump=True).exclude(id=r.id).update(is_active_dump=False)

    except Exception as e:
        pass
