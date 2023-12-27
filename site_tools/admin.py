from django.contrib import admin
from .forms import CatalogAdminForm, ReportCatalogAdminForm
from .models import Catalog, ReportCatalog


class CatalogAdmin(admin.ModelAdmin):
    form = CatalogAdminForm
    readonly_fields = ('status', 'uploaded_at', 'header_df')

    fieldsets = (
        (None, {
            'fields': (),
            'description': 'Информационный текст в шапке формы',
        }),
        ('Информация', {
            'fields': ('catalog',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('catalog',)
        return ()


class ReportCatalogAdmin(admin.ModelAdmin):
    form = ReportCatalogAdminForm
    readonly_fields = ('uploaded_at', 'report',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(ReportCatalog, ReportCatalogAdmin)
