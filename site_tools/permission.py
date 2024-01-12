from functools import wraps
from django.shortcuts import redirect


def load_dump_catalog_parm(user):
    if user.is_superuser:
        return True


def load_dump_catalog_permission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not load_dump_catalog_parm(request.user):
            return_url = request.META.get('HTTP_REFERER', None)
            if return_url:
                return redirect(return_url)
            else:
                return redirect('shop:categories')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
