from django import template
from django.contrib.auth.models import User
from exams.models import ExamResult, Exam, FailedTest
from django.utils.timezone import now, timedelta
from datetime import datetime

register = template.Library()


@register.filter(name='is_failed')
def failed(failed: FailedTest, user: User) -> int:
    """ return CODE
    [0] => successfull
    [1] => first try unsuccesfull
    [2] => second try unsuccessful

    """
    exam = failed.failed_exam
    result = ExamResult.objects.filter(exam=exam, user_id=user.id)
    if result.exists():

        return int(result.take)



@register.filter(name='get_time')
def get_time_failed(failed: FailedTest, user: User):

    exam = failed.failed_exam
    if ExamResult.objects.filter(exam=exam).exists():
       return ExamResult.objects.get(exam=exam, user_id=user.id).lock

@register.filter(name='is_timed')
def is_timed(failed: FailedTest, user: User):
    # print(type(ExamResult.objects.get(exam=exam_).lock_date))
    # print(ExamResult.objects.get(exam=exam_).lock_date)
    # print(datetime.today().date())
    # print(type(datetime.today().date()))
    # print(ExamResult.objects.get(exam=exam_).lock_date >= datetime.today())
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


