from .models import *
from django.utils.html import format_html
from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .forms import AdminFormGroup, AdminFormProduct, AdminFormCategory
from decimal import Decimal


class DownloadFileWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            return mark_safe(f'<a href="{value.url}" download>{value.name}</a>')
        else:
            return 'No file'


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('image_preview',)
    list_display = ['site_name', 'image_preview', 'art', 'is_active']
    exclude = ('slug',)
    form = AdminFormCategory
    fieldsets = (
        (None, {
            'fields': (),
            'description': 'Информационный текст в шапке формы',
        }),

        ('Информация о товаре', {
            'fields': ('name', 'site_name', 'image_preview', 'image', 'slug','art'),
        }),

        ('Архив', {
            'fields': ('is_active',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return self.readonly_fields + ('art', 'slug', 'name',)
        return self.readonly_fields + ('slug',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        else:
            return 'Фото не загружено'

    image_preview.short_description = 'Загруженное фото'


class GroupAdmin(admin.ModelAdmin):
    form = AdminFormGroup
    readonly_fields = ('image_preview',)
    list_display = ['site_name', 'image_preview', 'art', 'category', 'is_active']
    exclude = ('slug',)
    fieldsets = (
        (None, {
            'fields': (),
            'description': 'Информационный текст в шапке формы',
        }),
        ('Информация о товаре', {
            'fields': ('name', 'site_name', 'image_preview', 'image', 'slug','art'),
        }),
        ('Принадлежность к категории', {
            'fields': ('category',),
        }),
        ('Архив', {
            'fields': ('is_active',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return self.readonly_fields + ('art', 'slug', 'name')
        return self.readonly_fields + ('slug',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        else:
            return 'Фото не загружено'

    image_preview.short_description = 'Загруженное фото'


class ImagesProductsShopInline(admin.TabularInline):
    model = ImagesProductsShop
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        else:
            return '-'

    image_preview.short_description = 'Изображение'


class ProductAdmin(admin.ModelAdmin):
    form = AdminFormProduct
    inlines = [ImagesProductsShopInline]
    readonly_fields = ('image_preview',)
    search_fields = ['site_name__icontains']


    list_display = ['site_name', 'image_preview', 'art', 'group', 'is_active']
    fieldsets = (
        (None, {
            'fields': (),
            'description': 'Информационный текст в шапке формы',
        }),
        ('Информация о товаре', {
            'fields': ('name',
                       'site_name',
                       'art', 'price',
                       'old_price',
                       'stock',
                       'image_preview',
                       'image',
                       'slug',
                       'sv_site_name'
                       ),
        }),
        ('Акции', {
            'fields': ('promo_group',),
        }),
        ('Принадлежность к группе', {
            'fields': ('group',),
        }),
        ('Архив', {
            'fields': ('is_active',),
        }),
    )

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return self.readonly_fields + ('art', 'name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        else:
            return 'Фото не загружено'

    image_preview.short_description = 'Загруженное фото'


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('art', 'site_name', 'price', 'old_price', 'price_difference')
    readonly_fields = [f.name for f in Product._meta.fields] + ['price_difference']
    max_num = 0

    def price_difference(self, instance):
        if instance.price and instance.old_price:

            price = Decimal(instance.price)
            old_price = Decimal(instance.old_price)

            if price < old_price:
                return f'{abs(round(((price - old_price) / old_price) * 100, 2))}%'

        return 'Рекомендовано убрать из акции'

    price_difference.short_description = 'Разница'


class PromoProductGroupAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    exclude = ('products',)


admin.site.register(PromoProductGroup, PromoProductGroupAdmin)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Group, GroupAdmin)


