# -*- coding: utf-8 -*-
from unittest import TestCase

from orm import table
from orm import exceptions
from orm import fields


class TableTestCase(TestCase):

    def test_without_fields(self):
        with self.assertRaises(exceptions.NoFieldsError):
            class MyTable(table.Table):
                b = 12

    def test_normal_table(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 20)
            age = fields.IntegerField(99)

            c = 14

    def test_field_inheritance(self):

        class Person(table.Table):

            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 20)
            age = fields.IntegerField(99)

        class Employee(Person):
            job = fields.CharField('Developer')

        employee = Employee()
        for key in ('first_name', 'last_name', 'age', 'job'):
            self.assertIn(key, Employee._table_fields)
            self.assertIn(key, employee._table_fields)

    def test_inheritance_without_extra_fields(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 20)

        class Citizen(Person):
            pass

        citizen = Citizen()
        for key in ('first_name', 'last_name'):
            self.assertIn(key, citizen._table_fields)

    def test_class_has_got_sql(self):
        class Person(table.Table):
            first_name = fields.CharField('John')
            last_name = fields.CharField('Doe')

        self.assertTrue(hasattr(Person, 'sql'))

    def test_instance_has_not_got_sql(self):
        class Person(table.Table):
            first_name = fields.CharField('John')
            last_name = fields.CharField('Doe')

        person = Person()

        self.assertFalse(hasattr(person, 'sql'))

    def test_sql(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 50)
            age = fields.IntegerField(18)

        sql = Person.sql

        for items in ('Person', 'Varchar(20)', 'Varchar(50)', 'Integer',
                      'first_name', 'last_name', 'age'):
            self.assertIn(items, sql)

    def test_get_for_instance(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 50)
            age = fields.IntegerField(18)

        person = Person()
        self.assertEquals(person.age, 18)
        self.assertEquals(person.first_name, 'John')
        self.assertEquals(person.last_name, 'Doe')

    def test_set_for_instance(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 50)
            age = fields.IntegerField(18)

        person  = Person()
        person.first_name = 'Ivan'
        person.last_name = 'Sidorov'
        person.age = 32

    def test_validation_errors(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 50)
            age = fields.IntegerField(18)

        person = Person()

        for attr, value in (('first_name', 23), ('last_name', []),
                            ('age', 'blabla')):
            with self.assertRaises(exceptions.ValidationError):
                setattr(person, attr, value)

    def test_independence(self):
        class Person(table.Table):
            first_name = fields.CharField('John', 20)
            last_name = fields.CharField('Doe', 50)
            age = fields.IntegerField(18)

        john = Person()
        nick = Person()

        self.assertNotEquals(id(john), id(nick))

        john.age = 22
        nick.first_name = 'Nick'

        self.assertEquals(john.age, 22)
        self.assertEquals(nick.age, 18)
        self.assertEquals(john.first_name, 'John')
        self.assertEquals(nick.first_name, 'Nick')



