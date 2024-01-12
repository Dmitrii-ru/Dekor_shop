from django.urls import path, include
from .views import *

app_name = 'shop'

urlpatterns = [
    path('www', index, name='www'),
    path('products/promo', PromoProductList.as_view(), name="promo_product"),
    path('products/search', SearchProduct.as_view(), name='search'),
    path('<slug_category>/<slug_group>/<slug:slug>', ProductDetail.as_view(), name='product'),
    path('<slug_category>/<slug_group>', ProductsList.as_view(), name='products'),
    path('<slug_category>', GroupList.as_view(), name='groups'),
    path('', CategoryList.as_view(), name='categories'),

]
