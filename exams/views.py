
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .exam_data_class import ExamOverview, Test, ExamValidation
from .models import Exam, ExamResult, AviableTest, FailedTest, CompleteTest
from lessons.models import Lesson


def can_user_be_here(user, lesson_id):
    exam = Exam.objects.get(exam_number=lesson_id)
    aviable = AviableTest.objects.filter(user=user, aviable_exam=exam)
    if aviable.exists():
        return True
    failed = FailedTest.objects.filter(user=user, failed_exam=exam)
    if failed.exists():
        if failed.get().take < 3:
            return False

    complete = CompleteTest.objects.filter(user=user, complete_exam=exam)
    if complete.exists():
        return False
    return True


@login_required(login_url='/accounts/login/')
def exam_view(request, lesson_id):
    """stránka se samotným testem"""

    # aviability TODO pokud u6ivatel nem8 povolen vstup
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
    """přehled dostupných a splněných testů"""

    exams = ExamOverview(request.user)
    return render(request, 'exams/all.html', {'exams': exams})


@login_required(login_url='/accounts/login/')
def exam_overview(request, lesson_id):
    """úvodní stránka než začne test"""
    exam = Exam.objects.get(id=lesson_id)
    if not can_user_be_here(request.user, lesson_id):
        return redirect('exams:all')
    return render(request, 'exams/welcome.html', {'exam': exam,
                                                  'lesson_id': lesson_id})


def result_view(request, lesson_id):
    """zobrazí výsledky jednoho testu"""
    # aviability
    if not ExamResult.objects.filter(user_id=request.user.id,
                                     exam=lesson_id).exists():
        return redirect('crossroad:overview')

    result = ExamResult.objects.get(exam=lesson_id, user_id=request.user.id)

    return render(request, 'exams/result.html', {'result': result})
