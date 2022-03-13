from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .exam_data_class import ExamOverview, Test, ExamValidation
from .models import Exam
from random import randint



@login_required(login_url='/accounts/login/')
def exam_view(request, lesson_id):


    # TODO udělat tři dict pro single, multi a pro tu poslední blbost
    if request.method == 'POST':
        POST_data_dict = []
        POST_data_open = {}

        for item in request.POST.keys():
            POST_data_dict.append(request.POST[item])
            if item == 'OPEN':
                POST_data_open['OPEN'] = request.POST[item]

        validator = ExamValidation(lesson_id, P)
        validator.load_data()
        a = validator.validate()
        print(a)
    data = Test(request.user, lesson_id)

    return render(request, 'exams/exam.html', {'data': data})




@login_required(login_url='/accounts/login/')
def exam_all(request):
    exams = ExamOverview(request.user)
    return render(request, 'exams/all.html', {'exams': exams})


@login_required(login_url='/accounts/login/')
def exam_overview(request, lesson_id):
    exam = Exam.objects.get(id=lesson_id)

    return render(request, 'exams/welcome.html', {'exam': exam,
                                                  'lesson_id': lesson_id})
