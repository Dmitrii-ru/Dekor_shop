from django import forms
from .models import Product, Group, Category, PromoProductGroup
from django.core.exceptions import ValidationError


class AdminFormProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'sv_site_name': forms.Textarea(attrs={'cols': 100, 'rows': 2}),
        }

    def clean_group(self):
        group = self.cleaned_data['group']
        if not group.is_active:
            raise ValidationError(f'Группа: "{group}" не доступна (В архиве)')
        return group


    def clean_old_price(self):
        model_meta = self.Meta.model._meta
        price = self.cleaned_data.get('price')
        old_price = self.cleaned_data.get('old_price')
        if old_price and price:
            if old_price <= price:
                raise ValidationError(f"Значение поля {model_meta.get_field('old_price').verbose_name} "
                                      f"не может быть больше чем поле "
                                      f"{model_meta.get_field('price').verbose_name}")

        return old_price


class AdminFormGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category.is_active:
            raise ValidationError(f'Категория: "{category}" не доступна (В архиве)')
        return category


class AdminFormCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AdminFormPromoProductGroup(forms.ModelForm):

    class Meta:
        model = PromoProductGroup
        fields = '__all__'