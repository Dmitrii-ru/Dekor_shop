from site_tools.utils.catalog.base_validator import ValidateTempObject
from site_tools.utils.catalog.search import get_base_form_words


class ObjectUpdate(ValidateTempObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields = []
        self.update_obj = kwargs.get('update_obj')
        self.is_active = self.update_obj.is_active


    def clean_name(self):
        super(ObjectUpdate, self).clean_name()
        _name = self.name
        if hasattr(self.model_name_field, 'unique'):
            if getattr(self.model_name_field, 'unique') and _name != self.update_obj.name:
                if _name in self.list_name:
                    raise ValueError(
                        self.create_error_message(
                            field_verb_name='name', message='not_unique', var=_name
                        )
                    )

        self.update_fields.append('name')
        self.update_obj.name = _name

    def clean_site_name(self):
        super(ObjectUpdate, self).clean_site_name()
        _site_name = self.site_name
        if hasattr(self.model_site_name_field, 'unique'):
            if getattr(self.model_site_name_field, 'unique') and _site_name != self.update_obj.site_name:
                if _site_name in self.list_site_name:
                    raise ValueError(
                        self.create_error_message(
                            field_verb_name='site_name', message='not_unique', var=_site_name
                        )
                    )

                self.update_fields.append('site_name')
                self.update_obj.site_name = self.site_name
                if hasattr(self.update_obj, 'sv_site_name'):
                    self.update_obj.sv_site_name = get_base_form_words(_site_name)
                    self.update_fields.append('sv_site_name')

    def clean_is_active(self):
        _is_active = self.is_active
        if not _is_active:
            self.report.new_record(
                self.model_django._meta.verbose_name_plural,
                'is_actual_true',
                1,
                self.update_obj
            )
            self.update_obj.is_active = _is_active
            self.update_fields.append('is_active')

    def clean_price(self):
        super(ObjectUpdate, self).clean_price()
        _price = self.price
        old_price = float(self.update_obj.price)
        if old_price != _price:
            if old_price <= _price:
                if self.update_obj.promo_group:
                    self.update_obj.promo_group = None
                    self.update_fields.append('promo_group')
                    self.report.new_record(
                        self.model_django._meta.verbose_name_plural,
                        'promotion_false',
                        2,
                        self.update_obj
                    )

            elif old_price < _price:
                self.update_obj.old_price = self.update_obj.price
                self.update_fields.append('old_price')
                self.report.new_record(
                    self.model_django._meta.verbose_name_plural,
                    'recomm_promotion',
                    3,
                    self.update_obj
                )

            self.update_obj.price = _price
            self.update_fields.append('price')

    def methods_clean(self):
        for attr_name in dir(self):
            if attr_name.startswith('clean_') and callable(getattr(self, attr_name)):
                field_name = attr_name.replace('clean_', '')
                if hasattr(self, field_name):
                    getattr(self, attr_name)()

    def update(self):
        self.methods_clean()
        if self.update_fields:
            self.models_dict['to_update'].setdefault(
                tuple(self.update_fields), []
            ).append(
                self.update_obj
            )
            self.models_dict['art_list'].append(self.update_obj.art)
        return self.update_obj
