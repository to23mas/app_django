from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson


@login_required(login_url='/accounts/login/')
def welcome_view(request):
    """app welcome page"""
    return render(request, 'crossroad/welcome.html')


@login_required(login_url='/accounts/login/')
def courses_overview_view(request):
    list_courses = Lesson.objects.all()

    return render(request, 'crossroad/courses_overview.html', {'lessons': list_courses, })


@login_required(login_url='/accounts/login/')
def about_view(request):
    return render(request, 'crossroad/about.html')
