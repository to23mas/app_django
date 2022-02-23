from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Chapter


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
    navbar = Chapter.objects.get(chapter_lesson_id=lesson_id)

    return render(request, 'lessons/main.html', {'lesson': lesson,
                                                 'navbar': navbar})
