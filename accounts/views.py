from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, logout
from .forms import CustomUserForm
from .validation import Validate
from lessons.unlock_progress import ProgressHandler


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


def welcome_view(request, project=1):
    """welcome page with twi links to signup  and register"""

    if request.user.is_authenticated:
        return redirect('crossroad:welcome')
    else:
        return render(request, 'accounts/welcome.html', {'project': project})


def register_view(request):
    """register page with form"""

    if request.user.is_authenticated:
        return redirect('crossroad:welcome')

    if request.method == 'POST':
        form = CustomUserForm(request.POST)


        if form.is_valid():
            user = form.save()
            login(request, user)  # přihlášení uživatele
            progress_handler = ProgressHandler(user=user, lesson_id=1)
            progress_handler.unlock_default() #odemik8 u6ivateli prvni dve lekce
            return redirect('crossroad:welcome')
    else:
        form = CustomUserForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request, project=1):

    if request.user.is_anonymous:
        return redirect('accounts:welcome', 1)
    logout(request)
    if project == 1:
        return redirect('accounts:welcome', 1)
    else:
        return redirect('accounts:welcome', 2)

def forgotten_password_view(request):
    if request.user.is_authenticated:
        return redirect('crossroad:welcome')

    error = ''
    if request.method == 'POST':
        error = Validate.validate_email(request.POST['email'])
        if error != '':
            return render(request, 'accounts/forgotten_password.html', {'form': PasswordResetForm(),
                                                                        'error': error})
        else:
            return render(request, 'accounts/password_send.html')


def redirect_logged_user(user):
    if user.is_authenticated:
        return redirect('crossroad:welcome')


def password_send_view(request):
    return render(request, 'accounts/password_send.html')
