"""
Views

Všechny views pro přihlašování odhlašování, nebo registaci

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserForm
from lessons.unlock_progress import ProgressHandler


def login_view(request):
    """ View pro přihlašovací obrazovku.
    Přihlášený uživatel přesměrován do aplikace

    @var form: přihlašovací formulář
    @var user: uživatel
    """

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
    """ View uvítací obrazovky. Přihlášeného uživatele rovnou přesměruje do vlastní aplikace
    Nepřihlášenému zobrazí stránku s výběrem registrace a přihlášení.
    """

    if request.user.is_authenticated:
        return redirect('crossroad:welcome')
    else:
        return render(request, 'accounts/welcome.html')


def register_view(request):
    """ View pro registraci.
    Přihlášený uživatel přesměrován do aplikace. Nově registovanému uživateli je přiřazena skupina,
     aby mohl navštívit první učební lekci

    @var form: registrační formulář
    @var user: uživatel
    @var progresshandler: instance třídy ProgressHandler odemyká první lekci
    """

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


def logout_view(request, ):
    """View pro funkci odhlášení"""
    if request.user.is_anonymous:
        return redirect('accounts:welcome')
    logout(request)

    return redirect('accounts:welcome', )


def welcome_project_view(request):
    """View odpovídá WELCOME_VIEW
    Je zde kvůli zobrazení jiné přihlašovací obrazovky. Uživatel se může dostat k lekc, kde se bude učit,
     jak vytvořit registrační formulář. Po kliknutí na tuto lekci bude přesměrován na uvítací s vysvětlujícím textem"""
    if request.user.is_authenticated:
        return redirect('crossroad:welcome')
    else:
        return render(request, 'accounts/welcomeP.html')


def logout_two_view(request):
    """Odhlašující View pro Projekt Account (ÚČTY)"""
    if request.user.is_anonymous:
        return redirect('accounts:welcome')

    logout(request)

    return redirect('accounts:welcomeProject')

