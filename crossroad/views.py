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
    listOne = list_courses[1]
    # row = list_courses.count() // 5 + 1
    row = 6 // 5 + 1
    rows = [i for i in range(row)]
    cols = [i for i in range(4)]
    return render(request, 'crossroad/courses_overview.html', {'lessons': list_courses,
                                                               'rows': rows,
                                                               'cols': cols, })


@login_required(login_url='/accounts/login/')
def about_view(request):
    return render(request, 'crossroad/about.html')
