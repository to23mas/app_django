from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Chapter, Requirements, Goals
from .allowed import is_user_allowed

@login_required(login_url='/accounts/login/')
def welcome_view(request, lesson_id):
    """app welcome page"""

    lesson = Lesson.objects.get(pk=lesson_id)
    navbar = Chapter.objects.filter(chapter_lesson_id=lesson_id)
    return render(request, 'lessons/welcome.html', {'lesson': lesson,
                                                    'navbar': navbar})


# TODO
def chapter_view(request, lesson_id, chapter):

    lesson = Lesson.objects.get(pk=lesson_id)
    if not is_user_allowed(lesson, request.user):
        return render(request, 'crossroad/welcome.html')

    navbar = Chapter.objects.filter(chapter_lesson_id=lesson_id).order_by('-id')
    requirements = Requirements.objects.filter(req_lesson_id=lesson_id)
    goals = Goals.objects.filter(goal_lesson_id=lesson_id)

    return render(request, 'lessons/main.html', {'lesson': lesson,
                                                 'navbar': navbar,
                                                 'chapter': chapter,
                                                 'requirements': requirements,
                                                 'goals': goals,
                                                 })
