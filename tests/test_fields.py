# -*- coding: utf-8 -*-
from unittest import TestCase
from orm import fields
from orm import exceptions


class FieldTestCase(TestCase):

    def test_check_value_error(self):
        class ErrorField(fields.Field):
            def check_value(self, value):
                raise exceptions.ValidationError("Error")

            @property
            def sql_type(self):
                return 'Integer'

        with self.assertRaises(exceptions.ValidationError):
            ErrorField(1)

    def test_check_value_success(self):
        class SuccessField(fields.Field):
            def check_value(self, value):
                pass

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


class IntegerFieldTestCase(TestCase):

    def test_wrong_values(self):
        for value in ('asd', '123', object, 43.12, [1, 2]):
            with self.assertRaises(exceptions.ValidationError):
                fields.IntegerField(value)

    def test_correct_value(self):
        fields.IntegerField(12)

    def test_sql_type(self):
        field = fields.IntegerField(24)
        self.assertEquals(field.sql_type, 'Integer')

    def test_wrong_value_set(self):
        field = fields.IntegerField(1)
        with self.assertRaises(exceptions.ValidationError):
            field.value = "Blablabla"

    def test_right_value_set(self):
        field = fields.IntegerField(1)
        field.value = 50


class CharFieldTestCase(TestCase):

    def test_wrong_values(self):
        for value in (1, 12.32, object, True, []):
            with self.assertRaises(exceptions.ValidationError):
                fields.CharField(value)

    def test_correct_value(self):
        fields.CharField('value')

    def test_sql_type(self):
        field = fields.CharField('value')
        self.assertEquals(field.sql_type, 'Varchar(255)')

    def test_wrong_max_length_values(self):
        for max_length in (object, -12, "128"):
            with self.assertRaises(exceptions.InitialError):
                fields.CharField('value', max_length=max_length)

    def test_correct_max_length_value(self):
        fields.CharField('value', 128)

    def test_wrong_value_length(self):
        with self.assertRaises(exceptions.ValidationError):
            fields.CharField('mother', max_length=2)

    def test_right_value_length(self):
        fields.CharField('mother', max_length=10)

    def test_max_length_sql_type(self):
        field = fields.CharField('mother', max_length=128)
        self.assertEquals(field.sql_type, 'Varchar(128)')

    def test_wrong_value_set(self):
        field = fields.CharField("mother", 10)
        with self.assertRaises(exceptions.ValidationError):
            field.value = object

        with self.assertRaises(exceptions.ValidationError):
            field.value = 'abcdefghijklmnopqrstuvwxyz'
