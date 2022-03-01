from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Chapter, Requirements, Goals, Content
from .allowed import is_user_allowed
from .unlock import Aviability_Handler


@login_required(login_url='/accounts/login/')
def welcome_view(request, lesson_id):
    """app welcome page"""

    lesson = Lesson.objects.get(pk=lesson_id)
    navbar = Chapter.objects.filter(chapter_lesson_id=lesson_id)
    return render(request, 'lessons/welcome.html', {'lesson': lesson,
                                                    'navbar': navbar})


# TODO
def chapter_view(request, lesson_id, chapter_name):

    if request.method == 'POST':
        chapter_name = Aviability_Handler.unlock_chapter_by_reading(request.user, chapter_name, lesson_id)

    lesson = Lesson.objects.get(pk=lesson_id)
    if not is_user_allowed(lesson, request.user):
        return render(request, 'crossroad/welcome.html')

    chapters = Chapter.objects.filter(chapter_lesson_id=lesson_id).order_by('-id')
    requirements = Requirements.objects.filter(req_lesson_id=lesson_id)
    goals = Goals.objects.filter(goal_lesson_id=lesson_id)

    # tohle není uplně obratné..... hledám id abych pak našel content možná půjde přes ORM TODO
    chapter = Chapter.objects.get(chapter_lesson_id=lesson_id, chapter_link=chapter_name)

    return render(request, 'lessons/main.html', {'lesson': lesson,
                                                 'chapters': chapters,
                                                 'chapter_name': chapter_name,
                                                 'requirements': requirements,
                                                 'goals': goals,
                                                 'chapter': chapter
                                                 })
