from site_tools.utils.catalog.base_validator import ValidateTempObject
from site_tools.utils.catalog.search import get_base_form_words


class ObjectCreate(ValidateTempObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_name(self):
        super(ObjectCreate, self).clean_name()
        _name = self.name
        if hasattr(self.model_name_field, 'unique'):
            if getattr(self.model_name_field, 'unique'):
                if _name in self.list_name:
                    raise ValueError(
                        self.create_error_message(
                            field_verb_name='name', message='not_unique', var=_name
                        )
                    )

    def clean_site_name(self):
        super(ObjectCreate, self).clean_site_name()
        _site_name = self.site_name
        if hasattr(self.model_site_name_field, 'unique'):
            if getattr(self.model_site_name_field, 'unique'):
                if _site_name in self.list_site_name:
                    raise ValueError(
                        self.create_error_message(
                            field_verb_name='site_name', message='not_unique', var=_site_name
                        )
                    )


    def clean_art(self):
        super(ObjectCreate, self).clean_art()

    def clean_slug(self):
        super(ObjectCreate, self).clean_slug()

    def clean_price(self):
        super(ObjectCreate, self).clean_price()

    def clean_unit(self):
        super(ObjectCreate, self).clean_unit()

    def clean_old_price(self):
        super(ObjectCreate, self).clean_old_price()

    def clean_sv_site_name(self):
        super(ObjectCreate, self).clean_sv_site_name()
        _site_name = get_base_form_words(self.site_name)
        setattr(self, 'sv_site_name', _site_name)

    def clean_category(self):
        super(ObjectCreate, self).clean_category()

    def clean_group(self):
        super(ObjectCreate, self).clean_group()

    def methods_clean(self):
        for attr_name in dir(self):
            if attr_name.startswith('clean_') and callable(getattr(self, attr_name)):
                field_name = attr_name.replace('clean_', '')
                if hasattr(self, field_name):
                    getattr(self, attr_name)()

    def create(self):
        self.methods_clean()
        model_fields = [field.name for field in self.model_django._meta.get_fields()]
        kwargs = {field: getattr(self, field) for field in model_fields if hasattr(self, field)}
        obj = self.model_django(**kwargs)
        self.report.new_record(
            self.model_django._meta.verbose_name_plural,
            'new',
            4,
            self
        )
        self.models_dict['art_list'].append(obj.art)

        return obj
