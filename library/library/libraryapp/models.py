from django.db import models


class Person(models.Model):
    first_name = models.CharField(
        verbose_name='First name',
        max_length=255
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=255
    )


class Reader(models.Model):
    person = models.OneToOneField(Person)


class Author(models.Model):
    person = models.OneToOneField(Person)


class Bookshelf(models.Model):
    name = models.CharField(
        verbose_name='Shelf name',
        max_length=255
    )


class Book(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )
    authors = models.ManyToManyField(Author)
    bookshelf = models.ForeignKey(Bookshelf, db_index=True)
    reader = models.ForeignKey(Reader, blank=True, null=True)

