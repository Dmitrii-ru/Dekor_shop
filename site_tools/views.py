import os

from django.shortcuts import render
from site_tools.utils.catalog.catalog_upload_v3 import transaction_upload_catalog_test
def test_catalog(request):
    transaction_upload_catalog_test(os.path.abspath("Тест каталог.xlsx"))
    return render(request, 'site_tools/index.html')
