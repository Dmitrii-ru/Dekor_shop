from django.shortcuts import render, redirect
from .permission import load_dump_catalog_permission
from .tasks import call_command_catalog_load_task


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
