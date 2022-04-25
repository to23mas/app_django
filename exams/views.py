"""
Views

Views pro práci s testy.


@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .exam_data_class import ExamOverview, Test, ExamValidation
from .models import Exam, ExamResult, AviableTest, FailedTest, CompleteTest



def can_user_be_here(user, lesson_id):
    """ funkce kontrolující, jestli uživatel vůbec může psát daný test
    @param user: uživatel
    @param lesson_id id lekce

    @return True pokud uživatel test psát nemůže
            false, pokud může
    """
    exam = Exam.objects.get(exam_number=lesson_id)
    aviable = AviableTest.objects.filter(user=user, aviable_exam=exam)
    if aviable.exists():
        return True
    failed = FailedTest.objects.filter(user=user, failed_exam=exam)
    if failed.exists():
        if failed.get().take < 3:
            return True

    complete = CompleteTest.objects.filter(user=user, complete_exam=exam)
    if complete.exists():
        return True
    return False


@login_required(login_url='/accounts/login/')
def exam_view(request, lesson_id):
    """view pro stránku se samotným testem.

    @var validator: instance třídy ExamValidation
                      nejdříve načte data, poté zvaliduje.

    @var test: předatavuje data testu

    @param lesson_id: id příslušné lekce

    přesměrování na výsledky testu.
    """

    if not can_user_be_here(request.user, lesson_id):
        return redirect('exams:result', lesson_id)



    if request.method == 'POST':
        validator = ExamValidation(lesson_id, request.POST)
        validator.load_data()
        validator.validate()
        validator.result(request.user.id)
        return redirect('exams:result', lesson_id)

    test = Test(request.user, lesson_id)

    return render(request, 'exams/exam.html', {'data': test})


@login_required(login_url='/accounts/login/')
def exam_all(request):
    """view sobrazuje seznam dostupných testů"""

    exams = ExamOverview(request.user)
    return render(request, 'exams/all.html', {'exams': exams})


@login_required(login_url='/accounts/login/')
def exam_overview(request, lesson_id):
    """View pro stránku s úvodem do testu, který se uživatel chystá psát

    @param lesson_id: id likce pro nalezení příslušného testu
    """
    exam = Exam.objects.get(id=lesson_id)
    if not can_user_be_here(request.user, lesson_id):
        return redirect('exams:all')
    return render(request, 'exams/welcome.html', {'exam': exam,
                                                  'lesson_id': lesson_id})

@login_required(login_url='/accounts/login/')
def result_view(request, lesson_id):
    """View se stránkou s výsledkem testu
    @param lesson_id: id lekce , podle kterého se zništťuje, který test se má zobrazit
    @var result: výsledek testu
    """

    if not ExamResult.objects.filter(user_id=request.user.id,
                                     exam=lesson_id).exists():
        return redirect('crossroad:overview')

    result = ExamResult.objects.get(exam=lesson_id, user_id=request.user.id)

    return render(request, 'exams/result.html', {'result': result})
