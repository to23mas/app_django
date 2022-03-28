from django import template
from django.contrib.auth.models import User
from lessons.models import Lesson
from exams.models import CompleteTest

register = template.Library()


@register.filter(name='has_group')
def has_group(user: User, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_competed')
def is_completed(user: User, lesson: Lesson) -> bool:
    complete = CompleteTest.objects.filter(user_id=user.id, complete_exam_id=lesson.id)

    return True if complete.exists() else False

