from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson
from django.contrib.auth.models import User


def is_user_allowed(lesson: Lesson, user: User) -> bool:
    if user in lesson.allowed.all():
        return True
    return False
