"""
Models

model pro aplikaci projekts

classes: Ukol, Soubor, Project, Useraccount

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""

from django.db import models
from django.contrib.auth.models import User
from lessons.models import Lesson


class Ukol(models.Model):
    """Třída představující záznamy v úkolníčku, tedy jednotlivé úkoly.

        @param  typy: jednotlivé úkoly mohou mít různé typy
        @param  text: vlastní text úkolu
        @param  typ: přiřazený typ k úkolu
        @param  user: představuje uživatele který úkol uložil

        """

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
    """Třída představující soubory, pro ukládání souborů do databáze
        @param  lesson: k jaké lekci soubor patří
        @param  name: název souboru
        @param  file: samotný soubor

    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    file = models.FileField()

    def __str__(self):
        """funkce pro výpis -> NÁZEV LEKCE - NÁZEV SOUBORU"""

        return f"{self.lesson.lesson_name} - {self.name}"


class Project(models.Model):
    """Třída představující přiřazení uživatele k projektu jednotlivé projekty. ManyToMany.

        @param  lesson: id lekce
        @param  user: id uživatele

    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """funkce pro výpis -> NÁZEV LEKCE - JMÉNO UŽIVATELE"""

        return f"{self.lesson.lesson_name} - {self.user.username}"


class UserAccount(models.Model):
    """Pro projekt kde uživatel přidává uživatele... třída představuje tyto přidané uživatele

        @param  jmeno: jmeno přidaného uživatele
        @param  email: email
        @param  heslo: heslo
        @param  heslo_znovu: heslo pro kontrolu


    """
    jmeno = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    heslo = models.CharField(max_length=50)
    heslo_znovu = models.CharField(max_length=50)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """funkce pro výpis -> NEW - JMENO_VYTVORENEHO_UCTU / YOU - JMENO TOHO, KDO VYTVÁŘEL"""
        return f"new - {self.jmeno} / you - {self.user.username}"
