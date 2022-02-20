from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import user_passes_test

def login_view(request):
    """pro login"""

    if request.user.is_authenticated:
        return redirect('crossroad:welcome')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # přihlášení uživatele
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('crossroad:welcome')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def welcome_view(request):
    """welcome page with twi links to signup  and register"""
    if request.user.is_authenticated:
        return redirect('crossroad:welcome')

    return render(request, 'accounts/welcome.html')


def register_view(request):
    """register page with form"""

    if request.user.is_authenticated():
        return redirect('crossroad:welcome')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # přihlášení uživatele
            #  log the user in
            return redirect('crossroad:welcome')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:welcome')


