from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def welcome_view(request):
    """app welcome page"""
    return render(request, 'crossroad/welcome.html')
