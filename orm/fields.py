# -*- coding: utf-8 -*-
from . import exceptions


class Field(object):

    default = None
    python_type = object
    _value = None

    def __init__(self, default):
        self.value = default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """
        Checks value and set value to value attribute
        :param value:
        :return: None
        """
        self.check_value(value)
        self._value = value

    def check_value(self, value):
        """
        Checks value. if values isn't correct raise exception.ValidationError
        :param value:
        :return: None
        """
        if not isinstance(value, self.python_type):
            raise exceptions.ValidationError((
                "{field_name} value should be "
                "{python_type_name} not {value_type_name}"
            ).format(**{
                'field_name': self.__class__.__name__,
                'python_type_name': self.python_type.__name__,
                'value_type_name': value.__class__.__name__
            }))

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


class CharField(Field):

    max_length = 255
    python_type = basestring

    def __init__(self, default, max_length=None):
        if not max_length is None:
            if not isinstance(max_length, int) or max_length < 1:
                raise exceptions.InitialError(
                    "max_length should be int and greater then 0"
                )
            self.max_length = max_length
        super(CharField, self).__init__(default)

    def check_value(self, value):
        super(CharField, self).check_value(value)
        if len(value) > self.max_length:
            raise exceptions.ValidationError(
                "Value shouldn't be longer then {} chars".format(
                    self.max_length
                )
            )

    @property
    def sql_type(self):
        return 'Varchar({})'.format(self.max_length)
