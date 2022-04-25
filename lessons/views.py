"""
Views

Views pro zobrazování, odemykání a posílání dat ohledně lekcí

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0

"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .allowed import is_user_allowed
from .unlock_progress import ProgressHandler
from .load_data_class import LessonData


@login_required(login_url='/accounts/login/')
def switch_view(request, lesson_id, chapter_link):
    """View pro přesměrovávání, aby nedocházelo k opetovnému odesílání formulářů"""
    if lesson_id == 1:
        return redirect('lessons:lessonOne', chapter_link=chapter_link)

    elif lesson_id == 2:
        return redirect('lessons:lessonTwo', chapter_link=chapter_link)
    elif 3 <= lesson_id <= 7:
        return redirect('lessons:project', chapter_link=chapter_link, lesson_id=lesson_id)
    else:
        return redirect('lessons:notLesson', not_='no')


@login_required(login_url='/accounts/login/')
def project_view(request, lesson_id, chapter_link):
    """View zaměřené na projekty.

    @param lesson_id: id lekce
    @param chapter_link: název prohlížené kapitoly

    @var data: data příslušné lekce - kapitoly, texty, obrázky
    @var hint: nápověda k otázce
    @var progress_handler = ProgressHandler má na starosti odemykání zamčeného obsahu

    """
    data = LessonData(lesson_id, chapter_link, request.user)
    hint = ''
    if request.method == 'POST':
        progress_handler = ProgressHandler(user=data.user, lesson_id=lesson_id)
        if 'text' in request.POST:
            if progress_handler.unlock_by_text(request.POST['text'], data.chapter.chapter_order):
                data.set_chapter(data.get_next_chapter())
            else:
                hint = progress_handler.hint
        elif 'exam' in request.POST:
            a = progress_handler.unlock_test()
            if a == 1:
                return redirect('crossroad:welcome')
            else:
                return redirect('exams:welcome', lesson_id=data.lesson.id)



        elif 'read':
            next_lesson = progress_handler.unlock_next_chapter(data.chapter.chapter_order)
            return redirect('lessons:switch',
                            lesson_id=data.lesson.id,
                            chapter_link=next_lesson)

    return render(request, 'lessons/project.html', {'lesson': data.lesson,
                                                    'chapters': data.chapters,
                                                    'chapter_link': chapter_link,
                                                    'requirements': data.requirements,
                                                    'goals': data.goals,
                                                    'chapter': data.chapter,
                                                    'is_complete': data.chapter_is_complete,
                                                    'hint': hint
                                                    })

@login_required(login_url='/accounts/login/')
def lessonOne_view(request, chapter_link):
    """View zaměřené na první lekci, první lekce má jinou strukturu
        než dvšechny ostatní a tak potřebuje vlastní view

        @param lesson_id: id lekce
        @param chapter_link: název prohlížené kapitoly

        @var data: data příslušné lekce - kapitoly, texty, obrázky
        @var hint: nápověda k otázce
        @var progress_handler = ProgressHandler má na starosti odemykání zamčeného obsahu

        """
    data = LessonData(1, chapter_link, request.user)
    hint = ''
    # odkliknutí tlačítka přečteno
    if request.method == 'POST':
        progress_handler = ProgressHandler(user=data.user, lesson_id=1)

        if 'text' in request.POST:
            if progress_handler.unlock_first_by_text(request.POST['text'], data.chapter.chapter_order):
                data.set_chapter(data.get_next_chapter())
            else:
                hint = 'Tak takhle se asi nejmenuješ'

        elif 'exam' in request.POST:
            a = progress_handler.unlock_first_test(1)
            if a == 1:
                return redirect('crossroad:welcome')
            else:
                return redirect('exams:welcome', lesson_id=data.lesson.id)

        elif 'read':
            next_lesson = progress_handler.unlock_next_chapter(data.chapter.chapter_order)

            return redirect('lessons:switch',
                            lesson_id=data.lesson.id,
                            chapter_link=next_lesson)


    if not is_user_allowed(data.user, data.lesson.id, data.chapter):
        return render(request, 'crossroad/welcome.html')

    return render(request, 'lessons/uvod.html', {'lesson': data.lesson,
                                                 'chapters': data.chapters,
                                                 'chapter_link': chapter_link,
                                                 'requirements': data.requirements,
                                                 'goals': data.goals,
                                                 'chapter': data.chapter,
                                                 'is_complete': data.chapter_is_complete,
                                                 'hint': hint
                                                 })

@login_required(login_url='/accounts/login/')
def lessonTwo_view(request, chapter_link):
    """View zaměřené na druhou lekci, druhá lekce má jinou strukturu
            než dvšechny ostatní a tak potřebuje vlastní view

            @param lesson_id: id lekce
            @param chapter_link: název prohlížené kapitoly

            @var data: data příslušné lekce - kapitoly, texty, obrázky
            @var hint: nápověda k otázce
            @var progress_handler = ProgressHandler má na starosti odemykání zamčeného obsahu

            """
    data = LessonData(2, chapter_link, request.user)

    # odkliknutí tlačítka přečteno
    if request.method == 'POST':
        progress_handler = ProgressHandler(user=data.user, lesson_id=2)
        if 'exam' in request.POST:
            a = progress_handler.unlock_first_test(2)

            if a == 1:
                return redirect('crossroad:welcome')
            else:
                return redirect('exams:welcome', lesson_id=data.lesson.id)
        elif 'read':
            next_lesson = progress_handler.unlock_next_chapter(data.chapter.chapter_order)

            return redirect('lessons:switch',
                            lesson_id=data.lesson.id,
                            chapter_link=next_lesson)

    return render(request, 'lessons/setup.html', {'lesson': data.lesson,
                                                  'chapters': data.chapters,
                                                  'chapter_link': chapter_link,
                                                  'requirements': data.requirements,
                                                  'goals': data.goals,
                                                  'chapter': data.chapter,
                                                  'is_complete': data.chapter_is_complete,
                                                  })

@login_required(login_url='/accounts/login/')
def not_view(request, not_):
    """View pro případ že nějakej uličník zkusí podvádět"""
    return render(request, 'lessons/not.html')
