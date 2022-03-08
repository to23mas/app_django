from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/accounts/login/')
def exam_view(request, lesson_id):



    return render(request, 'exams/exam.html', {'id': lesson_id })

