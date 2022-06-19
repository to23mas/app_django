"""
modul rozšiřující funkcionality šablonovacího systému JINJA


@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""


from django import template
from django.contrib.auth.models import User
from exams.models import ExamResult, FailedTest
from datetime import datetime

register = template.Library()


@register.filter(name='is_failed')
def failed(failed: FailedTest, user: User) -> int:
    """  filter vrací  číslo, odpovídající pokusů, které uživatel potřeboval na splnění

    @param failed: neúspěšný test, u kterého nás zajímá, kolik má neúspěšných pokusů
    @param user: příslušný uživatel

    return CODE
    [0] => successfull
    [1] => first try unsuccesfull
    [2] => second try unsuccessful

    @return int == pokusy
            None pokud test neexistuje

    """
    exam = failed.failed_exam
    result = ExamResult.objects.filter(exam=exam, user_id=user.id)
    if result.exists():

        return int(result.take)



@register.filter(name='get_time')
def get_time_failed(failed: FailedTest, user: User):
    """  filter vrací  čas, kdy se zamčený test odemkne

        @param failed: zamčený test
        @param user: příslušný uživateů

        @return čas odemčení nebo None
    """
    exam = failed.failed_exam
    if ExamResult.objects.filter(exam=exam).exists():
        my_time = ExamResult.objects.get(exam=exam, user_id=user.id).lock

        return f'{my_time.hour + 2} : {my_time.strftime("%M")}'

@register.filter(name='is_timed')
def is_timed(failed: FailedTest, user: User):
    """  filter vrací , údaj o tom, jestli je test zamčený nebo ne

    @param failed: zamčený test
    @param user: příslušný uživateů

    @return True == odemčeno, False == zamčeno

    """
    exam = failed.failed_exam
    ex = ExamResult.objects.get(exam=exam, user_id=user.id)
    if ex.lock_date >= datetime.today().date():
        if ex.lock >= datetime.now().time():
            return False

    ex.take = 1
    failed.take = 2
    failed.save()
    ex.save()
    return True
