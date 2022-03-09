from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .exam_data_class import ExamOverview
from .models import Exam


@login_required(login_url='/accounts/login/')
def exam_view(request, lesson_id):

    return render(request, 'exams/exam.html', {'id': lesson_id})


@login_required(login_url='/accounts/login/')
def exam_all(request):
    exams = ExamOverview(request.user)
    return render(request, 'exams/all.html', {'exams': exams})


@login_required(login_url='/accounts/login/')
def exam_overview(request, lesson_id):
    exam = Exam.objects.get(id=lesson_id)

    return render(request, 'exams/welcome.html', {'exam': exam,
                                                  'lesson_id': lesson_id})
