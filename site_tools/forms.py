from django import forms
from django.core.exceptions import ValidationError
from .models import Catalog, ReportCatalog
from .utils.catalog.get_header_catalog import get_header_catalog


class CatalogAdminForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('catalog', 'header_df')
        widgets = {
            'header_df': forms.HiddenInput(),
        }

    def clean(self):
        catalog = self.cleaned_data['catalog']
        if not catalog:
            raise ValidationError("Вы ничего не загрузили")
        elif not str(catalog).endswith('.xlsx'):
            raise ValidationError("Это не Excel файл")
        self.header_df = get_header_catalog(catalog)
        return self.cleaned_data


class ReportCatalogAdminForm(forms.ModelForm):
    class Meta:
        model = ReportCatalog
        fields = '__all__'
