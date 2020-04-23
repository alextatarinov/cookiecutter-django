import unicodedata

from django.db import models


class LowerFieldDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner=None):
        if instance is None:
            return None
        return instance.__dict__[self.field.attname]  # noqa: WPS609

    def __set__(self, instance, value):
        instance.__dict__[self.field.attname] = self.field.to_python(value)  # noqa: WPS609


class EmailLowerCaseField(models.EmailField):
    def to_python(self, value):
        value = super().to_python(value)
        if value:
            value = unicodedata.normalize('NFKC', value)
            if hasattr(value, 'casefold'):  # noqa: WPS421
                value = value.casefold()
        return value

    def contribute_to_class(self, cls, name, **kwargs):  # noqa: WPS117
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.attname, LowerFieldDescriptor(self))
