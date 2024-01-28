import re
from pytils.translit import slugify

from site_tools.utils.constants import validate_upload_catalog
from site_tools.utils.messages.create_db_massege import create_message_db


class ValidateTempObject:
    def __init__(self, *args, **kwargs):
        self.model_django = self.model_django
        self.models_dict = kwargs['models_dict']
        self.report = kwargs['report']

        self.model_art_field = self.model_django._meta.get_field('art')
        self.model_name_field = self.model_django._meta.get_field('name')
        self.model_site_name_field = self.model_django._meta.get_field('site_name')
        self.plural = self.model_django._meta.verbose_name_plural

        self.list_name = self.models_dict['name_list']
        self.list_site_name = self.models_dict['site_name_list']

        self.art = kwargs['art']
        self.name = kwargs['name']
        self.site_name = kwargs['site_name']
        self.slug = kwargs.get('slug', None)

        if kwargs.get('is_active'):
            self.is_active = kwargs['is_active']
        if kwargs.get('group'):
            self.group = kwargs['group']
        if kwargs.get('category'):
            self.category = kwargs['category']
        if 'price' in kwargs:
            self.price = kwargs['price']
            self.model_price_field = self.model_django._meta.get_field('price')
        if 'unit' in kwargs:
            self.unit = kwargs['unit']
            self.model_unit_field = self.model_django._meta.get_field('unit')
        if 'stock' in kwargs:
            self.stock = kwargs['stock']
            self.model_stock_field = self.model_django._meta.get_field('stock')

    def create_error_message(self, field_verb_name, message, var=None):
        message = validate_upload_catalog.get(message, '')
        field_verb_name = self.model_django._meta.get_field(field_verb_name).verbose_name

        if var:
            var = f' {var}'
        else:
            var = ''
        mess = f'' \
               f'{self.plural} -> ' \
               f'{self.model_art_field.verbose_name} = {self.art} -> ' \
               f'Поле: "{field_verb_name}" ' \
               f'{message}{var}.'
        return mess

    def clean_art(self):
        if not self.art:
            raise ValueError(
                f'{self.plural} -> '
                f'Проверьте наличие артикула.'
            )

    def clean_name(self):
        _name = self.name
        if hasattr(self.model_name_field, 'blank'):
            if not getattr(self.model_name_field, 'blank') and not _name:
                raise ValueError(self.create_error_message(field_verb_name='name', message='pure'))

    def clean_site_name(self):
        _site_name = self.site_name
        if hasattr(self.model_site_name_field, 'blank'):
            if not getattr(self.model_site_name_field, 'blank') and not _site_name:
                raise ValueError(self.create_error_message(field_verb_name='site_name', message='pure'))

    def clean_unit(self):
        _unit = self.unit
        if hasattr(self.model_unit_field, 'blank'):
            if not getattr(self.model_unit_field, 'blank') and not _unit:
                raise ValueError(self.create_error_message(field_verb_name='unit', message='pure'))

        elif hasattr(self.model_unit_field, 'max_length'):
            max_length = getattr(self.model_unit_field, 'max_length')
            if len(_unit) > max_length:
                raise ValueError(
                    self.create_error_message(
                        field_verb_name='unit', message='>max_length', var=max_length
                    )
                )

    def clean_price(self):
        _price = self.price

        if hasattr(self.model_price_field, 'blank'):
            if not getattr(self.model_price_field, 'blank') and not _price:
                raise ValueError(self.create_error_message(field_verb_name='price', message='pure'))

        try:
            if not isinstance(_price, float):
                _price = re.sub(r'\s+', ' ', str(_price))
                _price = _price.replace(',', '.')
                setattr(self, 'price', float(_price))

        except ValueError:
            raise ValueError(self.create_error_message(field_verb_name='price', message='not_digit'))

    def clean_slug(self):
        try:
            if not self.slug:
                setattr(self, 'slug', slugify(self.name[30:] + str(self.art)))
        except ValueError as e:
            raise ValueError(self.create_error_message(field_verb_name='slug', message='slug', var=e))

    def clean_old_price(self):
        pass

    def clean_sv_site_name(self):
        pass

    def clean_category(self):
        pass

    def clean_group(self):
        pass
