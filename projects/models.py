import os
from django.db import models
from django.contrib.auth.models import User
from lessons.models import Lesson
from django.conf import settings


class Ukol(models.Model):
    typy = (
        ("DŮLEŽITÉ", 'Důležité'),
        ("OSTATNÍ", "ostatní"),
    )
    hotove = (
        ("ANO", 'ano'),
        ("NE", "ne"),
    )

    text = models.CharField(max_length=50)
    typ = models.CharField(max_length=10, default="OSTATNÍ", choices=typy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Soubor(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    file = models.FileField()

    def __str__(self):
        return f"{self.lesson.lesson_name} - {self.name}"


class Project(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lesson.lesson_name} - {self.user.username}"


class UserAccount(models.Model):
    jmeno = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    heslo = models.CharField(max_length=50)
    heslo_znovu = models.CharField(max_length=50)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"new - {self.jmeno} / you - {self.user.username}"
#
# class Acount(models.Model):
#     pass
#
# class Account(models.Model):
#     pass
