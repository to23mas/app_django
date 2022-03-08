from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson, Chapter, Requirements, Goals, Content
from .allowed import is_user_allowed
from .unlock import Aviability_Handler
from .load_data_class import LessonData


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
    data = LessonData(1, chapter_link, request.user)

    test_form_text = ''

    # odkliknutí tlačítka přečteno
    if request.method == 'POST':
        if 'text' in request.POST:
            if Aviability_Handler.unlock_by_text(request.POST['text'], data.user):
                data.set_chapter(data.get_next_chapter())
            test_form_text = 'Tak takhle se asi nejmenuješ'
        elif 'exam' in request.POST:
            return redirect('exams:exam', lesson_id=data.lesson.id)
        else:
            next_lesson = Aviability_Handler.unlock_chapter_by_reading(data.user, data)
            if Aviability_Handler.lesson_is_completed(data.user.progress.lesson01, data.lesson.le_capitols):
                return redirect('crossroad:overview')

            return redirect('lessons:switch',
                            lesson_id=data.lesson.id,
                            chapter_link=next_lesson)


    # TODO ještě vyhodit uživatele z kapitoly ne jenom z lekce
    if not is_user_allowed(data.user, data.lesson.id, data.chapter):
        return render(request, 'crossroad/welcome.html')

    return render(request, 'lessons/uvod.html', {'lesson': data.lesson,
                                                 'chapters': data.chapters,
                                                 'chapter_link': chapter_link,
                                                 'requirements': data.requirements,
                                                 'goals': data.goals,
                                                 'chapter': data.chapter,
                                                 'is_complete': data.chapter_is_complete,
                                                 'form_fail': test_form_text
                                                 })


def lessonTwo_view(request, chapter_link):
    data = LessonData(2, chapter_link, request.user)

    return render(request, 'lessons/setup.html', {'lesson': data.lesson,
                                                  'chapters': data.chapters,
                                                  'chapter_link': chapter_link,
                                                  'requirements': data.requirements,
                                                  'goals': data.goals,
                                                  'chapter': data.chapter,
                                                  'is_complete': data.chapter_is_complete,
                                                  })


def not_view(request, not_):
    return render(request, 'lessons/not.html')
