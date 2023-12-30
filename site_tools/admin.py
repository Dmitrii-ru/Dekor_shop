from django.contrib import admin
from .forms import CatalogAdminForm, ReportCatalogAdminForm
from .models import Catalog, ReportCatalog, ProcessesMessage


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
    change_form_template = 'admin/reportcatalog_change_form.html'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        odj = self.get_object(request, object_id)
        if odj.is_active_dump and request.user.is_superuser:
            extra_context['show_load_data_button'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_actions(self, request):
        if request.user.is_superuser:
            return super().get_actions(request)
        return None


class ProcessesMessageAdmin(admin.ModelAdmin):
    model = ProcessesMessage
    readonly_fields = ('uploaded_at', 'message',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        if request.user.is_superuser:
            return super().get_actions(request)
        return None

admin.site.register(Catalog, CatalogAdmin)
admin.site.register(ReportCatalog, ReportCatalogAdmin)
admin.site.register(ProcessesMessage, ProcessesMessageAdmin)
