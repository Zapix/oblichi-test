# -*- coding: utf-8 -*-
from unittest import TestCase
from orm import fields
from orm import exceptions


class FieldTestCase(TestCase):

    def test_check_value_error(self):
        class ErrorField(fields.Field):
            def check_value(self, value):
                return False

            @property
            def sql_type(self):
                return 'Integer'

        with self.assertRaises(exceptions.ValidationError):
            ErrorField(1)

    def test_check_value_success(self):
        class SuccessField(fields.Field):
            def check_value(self, value):
                return True

            @property
            def sql_type(self):
                return 'Integer'

        SuccessField(1)

    def test_get_sql_type(self):
        class IntegerField(fields.Field):
            def check_value(self, value):
                return True

            @property
            def sql_type(self):
                return 'Integer'

        field = IntegerField(1)
        self.assertEquals(field.sql_type, 'Integer')