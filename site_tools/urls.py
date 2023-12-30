from django.urls import path
from .views import *

app_name = 'site_tools'

urlpatterns = [
    path('test_catalog', test_catalog, name="test_catalog"),
    path('load_data_catalog', load_dump_catalog, name='load_dump_catalog')
]
