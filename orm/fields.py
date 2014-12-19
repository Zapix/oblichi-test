# -*- coding: utf-8 -*-
from . import exceptions


class Field(object):

    default = None
    python_type = object
    value = None

    def __init__(self, default):
        self._set_value(default)

    def _set_value(self, value):
        """
        Checks value and set value to value attribute
        :param value:
        :return: None
        """
        self._check_value(value)
        self.value = value

    def _check_value(self, value):
        """
        Checks value. if values isn't correct raise exception.ValidationError
        :param value:
        :return: None
        """
        if not self.check_value(value):
            raise exceptions.ValidationError((
                "{field_name} value should be "
                "{python_type_name} not {value_type_name}"
            ).format(**{
                'field_name': self.__class__.__name__,
                'python_type_name': self.python_type.__name__,
                'value_type_name': value.__class__.__name__
            }))

    def check_value(self, value):
        """
        Checks is value is correct for field. Could be overload
        :param value:
        :return: boolean
        """
        return isinstance(value, self.python_type)

    @property
    def sql_type(self):
        """
        Return SQL type for field. Should be implemented
        :return: basestring
        """
        raise NotImplementedError


class IntegerField(Field):
    python_type = int

    @property
    def sql_type(self):
        return 'Integer'
