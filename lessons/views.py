from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Chapter, Requirements, Goals, Content
from .allowed import is_user_allowed
from .unlock import Aviability_Handler, Checker


@login_required(login_url='/accounts/login/')
def switch_view(request, lesson_id, chapter_link):

    if lesson_id == 1:
        return redirect('lessons:lessonOne', chapter_link=chapter_link)

    elif lesson_id == 2:
        return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    # elif lesson_id == 3:
    #     return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    # elif lesson_id == 4:
    #     return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    # elif lesson_id == 5:
    #     return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    # elif lesson_id == 6:
    #     return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    # elif lesson_id == 7:
    #     return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    else:
        return redirect('lessons:notLesson', not_='no')


def lessonOne_view(request, chapter_link):
    lesson_id = 1
    user = request.user
    chapter = Chapter.objects.get(chapter_lesson_id=lesson_id, chapter_link=chapter_link)
    is_complete = Checker.is_chapter_completed(user, lesson_id, chapter.chapter_order)
    test_form_text = ''
    # odkliknutí tlačítka přečteno
    if request.method == 'POST':
        if 'read' in request.POST:
            chapter = Aviability_Handler.unlock_chapter_by_reading(user, chapter.chapter_order, lesson_id)
            return redirect('lessons:chapter', lesson_id=lesson_id, chapter_link=chapter.chapter_link)
        elif 'text' in request.POST:
            if Aviability_Handler.unlock_by_text(request.POST['text'], user):
                return redirect('crossroad:overview')
            test_form_text = 'Tak takhle se asi nejmenuješ'

    # TODO ještě vyhodit uživatele z kapitoly ne jenom z lekce
    if not is_user_allowed(request.user, lesson_id, chapter):
        return render(request, 'crossroad/welcome.html')

    lesson = Lesson.objects.get(pk=lesson_id)
    chapters = Chapter.objects.filter(chapter_lesson_id=lesson_id).order_by('-id')
    requirements = Requirements.objects.filter(req_lesson_id=lesson_id)
    goals = Goals.objects.filter(goal_lesson_id=lesson_id)

    return render(request, 'lessons/uvod.html', {'lesson': lesson,
                                                 'chapters': chapters,
                                                 'chapter_link': chapter_link,
                                                 'requirements': requirements,
                                                 'goals': goals,
                                                 'chapter': chapter,
                                                 'is_complete': is_complete,
                                                 'form_fail': test_form_text
                                                 })


def lessonTwo_view(request,  chapter_link):
    return render(request, 'lessons/setup.html')


def not_view(request, not_):
    return render(request, 'lessons/not.html')
