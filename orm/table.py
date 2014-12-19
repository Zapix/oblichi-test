# -*- coding: utf-8 -*-
from . import fields
from . import exceptions


class FieldDescriptor(object):


    def __init__(self, field):
        self.field = field
        self.data = {}

    def __get__(self, instance, owner):
        return self.data.get(instance, self.field.default)

    def __set__(self, instance, value):
        self.field.check_value(value)
        self.data[instance] = value



class MetaTable(type):

    def __new__(cls, name, bases, attrs):
        """
        Metaclass for tables.Checks has table got tables?
        Raises error if hasn't and table is not abstract,
        move table_fields into _table_fields attribute,
        """
        abstract = 'abstract' in attrs and attrs['abstract']

        if not '_table_fields' in attrs:
            attrs['_table_fields'] = {}

        table_fields = {
            key: value
            for key, value in attrs.iteritems()
            if isinstance(value, fields.Field)
        }

        # Get fields from parents
        for parent in bases:
            if isinstance(parent, MetaTable):
                table_fields.update(parent._table_fields)

        if len(table_fields) < 1 and not abstract:
            raise exceptions.NoFieldsError(
                "Table {} should have at least one field".format(name)
            )

        #Clear class from fields:
        attrs = {
            key: value
            for key, value in attrs.iteritems()
            if not key in table_fields
        }

        attrs['_table_fields'].update(table_fields)

        attrs.update({
            name: FieldDescriptor(field)
            for name, field in table_fields.iteritems()
        })

        if abstract:
            del attrs['abstract']

        return super(MetaTable, cls).__new__(cls, name, bases, attrs)

    @property
    def sql(cls):
        return 'CREATE TABLE `{table_name}` ({fields});'.format(
            table_name=cls.__name__,
            fields=", ".join((
                "`{}` {}".format(name, field.sql_type)
                for name, field in cls._table_fields.iteritems()
            ))
        )


class Table(object):
    abstract = True
    __metaclass__ = MetaTable

