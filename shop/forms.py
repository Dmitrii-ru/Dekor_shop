from django import forms
from .models import Product, Group, Category
from django.core.exceptions import ValidationError


class AdminFormProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_group(self):
        group = self.cleaned_data['group']
        if not group.is_active:
            raise ValidationError(f'Группа: "{group}" не доступна (В архиве)')
        return group


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

