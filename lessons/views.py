from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson


@login_required(login_url='/accounts/login/')
def welcome_view(request, lesson_id):
    """app welcome page"""

    lesson = Lesson.objects.get(pk=lesson_id)
    return render(request, 'lessons/welcome.html', {'lesson':lesson})

