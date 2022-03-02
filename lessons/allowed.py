from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Chapter
from django.contrib.auth.models import User


def is_user_allowed(user: User, lesson_id: int, chapter: Chapter) -> bool:
    lesson = Lesson.objects.get(id=lesson_id)

    try:
        belongs = user.groups.get(name=lesson.lesson_group)
    except:
        return False
    else:
        return True
