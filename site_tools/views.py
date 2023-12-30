import os
from django.shortcuts import render, redirect
from .permission import load_dump_catalog_permission
from site_tools.utils.catalog.catalog_upload_v3 import transaction_upload_catalog_test
from .tasks import call_command_catalog_load_task


def test_catalog(request):
    transaction_upload_catalog_test(os.path.abspath("Тест каталог.xlsx"))
    return render(request, 'site_tools/index.html')


@load_dump_catalog_permission
def load_dump_catalog(request):
    """
    Load dump Catalog, Group, Product
    """
    call_command_catalog_load_task.delay()

    return_url = request.META.get('HTTP_REFERER', None)
    if return_url:
        return redirect(return_url)
    else:
        return redirect('shop:categories')
