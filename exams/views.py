from django.db.models.functions import Pi
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .exam_data_class import ExamOverview, Test, ExamValidation
from .models import Exam, ExamResult
from json import dumps
from random import randint


@login_required(login_url='/accounts/login/')
def exam_view(request, lesson_id):
    """stránka se samotným testem"""

    # aviability TODO pokud u6ivatel nem8 povolen vstup
    result = ExamResult.objects.filter(user_id=request.user.id, exam=lesson_id)
    if result.exists():
        takes = ExamResult.objects.get(user_id=request.user.id, exam=lesson_id).take
        if takes > 1:

            return redirect('exams:result', lesson_id)

    if request.method == 'POST':
        validator = ExamValidation(lesson_id, request.POST)
        validator.load_data()
        validator.validate()
        validator.result(request.user.id)
        return redirect('exams:result', lesson_id)

    data = Test(request.user, lesson_id)

    return render(request, 'exams/exam.html', {'data': data})


@login_required(login_url='/accounts/login/')
def exam_all(request):
    """přehled dostupných a splněných testů"""
    timed_out = Exam
    exams = ExamOverview(request.user)
    return render(request, 'exams/all.html', {'exams': exams})


@login_required(login_url='/accounts/login/')
def exam_overview(request, lesson_id):
    """úvodní stránka než začne test"""
    exam = Exam.objects.get(id=lesson_id)

    return render(request, 'exams/welcome.html', {'exam': exam,
                                                  'lesson_id': lesson_id})


def result_view(request, lesson_id):
    """zobrazí výsledky jednoho testu"""
    # aviability
    if not ExamResult.objects.filter(user_id=request.user.id,
                                     exam=lesson_id).exists():
        return redirect('crossroad:overview')

    result = ExamResult.objects.get(exam=lesson_id)

    return render(request, 'exams/result.html', {'result': result})

def retake_view(request, lesson_id):
    if request.method == 'POST':
        validator = ExamValidation(lesson_id, request.POST, retake=True)
        validator.load_data()
        validator.validate()
        validator.result(request.user.id)
        return redirect('exams:result', lesson_id)

    data = Test(request.user, lesson_id)

    return render(request, 'exams/exam.html', {'data': data})
