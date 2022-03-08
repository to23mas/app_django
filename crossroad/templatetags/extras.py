from django import template
from django.contrib.auth.models import User
from lessons.models import Lesson

register = template.Library()


@register.filter(name='has_group')
def has_group(user: User, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_competed')
def is_completed(user: User, lesson: Lesson) -> bool:
    les = lesson.lesson_group
    progress = ''
    if les == 'UVOD':
        progress = user.progress.lesson01
    elif les == 'HELLO':
        progress = user.progress.lesson02
    elif les == '':
        pass
    elif les == '':
        pass
    elif les == '':
        pass
    elif les == '':
        pass
    else:
        pass

    if progress == lesson.le_capitols:
        return True
    return False
