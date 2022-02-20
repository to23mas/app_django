from django.shortcuts import render

def welcome(request):
    """app welcome page"""
    return render(request, 'crossroad/welcome.html')
