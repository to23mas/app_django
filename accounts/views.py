from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def login(request):
    """pro signup"""
    return render(request, 'accounts/login.html')


def welcome(request):
    """welcome page with twi links to signup  and register"""
    return render(request, 'accounts/welcome.html')


def register(request):
    """register page with form"""

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #  log the user in
            return redirect('crossroad:welcome')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
