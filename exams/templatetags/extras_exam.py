from django import template
from django.contrib.auth.models import User
from exams.models import ExamResult, Exam
from django.utils.timezone import now, timedelta
from datetime import datetime

register = template.Library()


@register.filter(name='is_failed')
def failed(exam_: Exam) -> int:
    """ return CODE
    [0] => successfull
    [1] => first try unsuccesfull
    [2] => second try unsuccessful

    """
    if ExamResult.objects.filter(exam=exam_).exists():
        result = ExamResult.objects.get(exam=exam_)


        if result.percentage >= 60:
            return 0
        else:
            if result.take == 1:
                return 1
            else:
                return 2


@register.filter(name='get_time')
def get_time_failed(exam_: Exam):

    if ExamResult.objects.filter(exam=exam_).exists():
       return ExamResult.objects.get(exam=exam_).lock

@register.filter(name='is_timed')
def is_timed(exam_: Exam):
    # print(type(ExamResult.objects.get(exam=exam_).lock_date))
    # print(ExamResult.objects.get(exam=exam_).lock_date)
    # print(datetime.today().date())
    # print(type(datetime.today().date()))
    # print(ExamResult.objects.get(exam=exam_).lock_date >= datetime.today())
    ex = ExamResult.objects.get(exam=exam_)
    if ex.lock_date >= datetime.today().date():
        if ex.lock >= datetime.now().time():
            return False

    ex.take = 1
    ex.save()
    return True

