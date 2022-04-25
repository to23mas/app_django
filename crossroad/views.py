"""
Views

Views pro aplikaci crossroad, která napomáhá k jednodušímu pohybu
  mezi jednotlivými aplikacemi. Nebo zobrazuje uvítací obrazovku

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson



@login_required(login_url='/accounts/login/')
def welcome_view(request):
    """View pro uvítací obrazovku"""
    return render(request, 'crossroad/welcome.html')

@login_required(login_url='/accounts/login/')
def courses_overview_view(request):
    """View pro výpis seznamu lekcí

    @var list_couerses: seznam lekci
    @var rows: napomáhá výpisu = počet řádků
    @var cols: napomáhá výpisu = počet sloupců
    """
    list_courses = Lesson.objects.all()

    row = 6 // 5 + 1
    rows = [i for i in range(row)]
    cols = [i for i in range(4)]
    return render(request, 'crossroad/courses_overview.html', {'lessons': list_courses,
                                                               'rows': rows,
                                                               'cols': cols })


@login_required(login_url='/accounts/login/')
def about_view(request):
    """ View pro stránku 'O mě'. """
    return render(request, 'crossroad/about.html')
