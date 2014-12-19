# -*- coding: utf-8 -*-
from . import exceptions


class Field(object):
    default = None
    python_type = object

    def __init__(self, default):
        self._check_value(default)

    def _check_value(self, value):
        """
        Checks value. if values isn't correct raise exception.ValidationError
        :param value:
        :return:
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
        Checks is value is correct for field. Should be implemented
        :param value:
        :return: boolean
        """
        raise NotImplementedError

    @property
    def sql_type(self):
        """
        Return SQL type for field. Should be implemented
        :return: basestring
        """
        raise NotImplementedError
