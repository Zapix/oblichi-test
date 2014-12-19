# -*- coding: utf-8 -*-
class BaseOrmException(Exception):
    """
    Base class for exceptions in orm
    """
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value


class ValidationError(BaseOrmException):
    pass


class InitialError(BaseOrmException):
    pass
