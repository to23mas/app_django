"""
modul rozšiřující funkcionality šablonovacího systému JINJA


@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""

from django import template
from django.contrib.auth.models import User
from lessons.models import Lesson
from exams.models import CompleteTest

register = template.Library()  # registruje rozžíření k ostatním


@register.filter(name='has_group')
def has_group(user: User, group_name: str) -> bool:
    """ filter pro skupiny, Vrací True, v případě že uživatel je přiřazen k dotazované skupině

    @param user: uživatel
    @param group_name: název skupiny, na kterou se dotazujem

    @return True pokud uživatel ke skupině patří
            False pokud ne
    """
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_competed')
def is_completed(user: User, lesson: Lesson) -> bool:
    """ filter pro dotaz, jestli příslušný uživatel splnil lekci, která se má zobrazit na obrazovku

    @param user: uživatel
    @param lesson: dotazovaná Lekce

    @return True pokud je lekce již splěná
            False pokud ne
    """
    complete = CompleteTest.objects.filter(user_id=user.id, complete_exam_id=lesson.id)

    return True if complete.exists() else False
