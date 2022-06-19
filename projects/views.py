"""
Views

Všechny views pro projekty

Projekty jsou - Helloworld, Úkolníček, Account


@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UkolForm, RegisterForm, LoginForm
from .models import Ukol, Project, UserAccount


@login_required(login_url='/accounts/login/')
def hello_view(request):
    """ View pro první projekt, kde je poze vypsán text

    @param request: request klienta
    @return: vrací html stránku s textem "hello, World."
    """
    return render(request, 'projects/hello_world.html')

@login_required(login_url='/accounts/login/')
def todo_view(request):
    """ View pro druhý projekt "úkolníček"

    Je zde formulář pro přidávání jednotlivých úkolů a
    zároveň jsou pod formulářem jednotlivé úkoly vypsány

    @param request: request klienta

    @var    form: Formulář pro Ukoly
            ukoly: jednotlivé úkoly, které si už uživatel přidal

    @return: vrací html stránku s formulářem a úkoly
    """
    form = UkolForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.instance.user = request.user
        form.save()

    ukoly = Ukol.objects.filter(user=request.user)
    return render(request, 'projects/todo.html', {'form': form,
                                                  'ukoly': ukoly})

@login_required(login_url='/accounts/login/')
def todo_two_view(request):
    """ View pro rozšířenou verzi úkolníčku.

    Lépe stilizovaný úkolníček pomocí css.
    Přidaná možnost mazání úkolů.

    @param request: request klienta

    @var    form: Formulář pro Ukoly
            ukoly: jednotlivé úkoly, které si už uživatel přidal

    @return:    1. v případě "POST' následuje redirekt sama na sebe
                2. jinak render html stránky s formulářem a úkoly
    """
    form = UkolForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.instance.user = request.user

        form.save()
        return redirect('projects:todo_two')

    ukoly = Ukol.objects.filter(user=request.user)
    return render(request, 'projects/todo_two.html', {'form': form,
                                                      'ukoly': ukoly})

@login_required(login_url='/accounts/login/')
def delete_todo(request, todo_id: int):
    """View pro mazání jednotlivých úkolů.

    Po smazání je potřeba redirect aby nešo dotaz odeslat reloadem stránky.

    @param request: request klienta
    @param todo_id: id pro úkol, který má být smazán
    @return: redirect na view pro projekt úkolníčku
    """
    Ukol.objects.get(id=todo_id).delete()
    return redirect('projects:todo_two')

@login_required(login_url='/accounts/login/')
def all_view(request):
    """View zobrazí uživateli všechny dostupné projekty

    @param  request: request klienta
    @var    projects: projekty které má uživatel odemknuté
    @return: render html stránky s dostupnými projekty
    """
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/all.html', {'projects': projects})

@login_required(login_url='/accounts/login/')
def cross_view(request):
    """View pro projekt "accounts"
    @return:    vrací html stránku s odkazem na registraci a na přihlášení
    """
    return render(request, 'projects/cross.html')

@login_required(login_url='/accounts/login/')
def accounts_login_one(request):
    """View pro projekt "Accounts". s možností přihlášení účtů, které si uživatel vytvořil.

    @param  request: request kienta
    @var:   form: formulář pro přihlášení
            fail: výpis v případě nepovedeného přihlášení
            users: účty které si uživatel registroval

    @return:    1. POST - redirect sama na sebe aby nebylo možné požadevek odesla znovu
                2. renderuje html stránku s formulářem pro přihlášení a se seznamem účtů, které si uživatel vytvořil.
    """

    form = LoginForm(request.POST or None, request.FILES or None)
    fail = ''
    if request.method == 'POST':

        form.user = request.user
        if login_form_check(form):
            fail = 'chybné heslo nebo jméno'

        else:
            return redirect('projects:done')

    users = UserAccount.objects.filter(user=request.user)
    return render(request, 'projects/account_login.html', {'form': form,
                                                           'fail': fail,
                                                           'users': users, })

@login_required(login_url='/accounts/login/')
def accounts_register_view(request):
    """View pro project "Accounts". Zde si uživatel zkouší registraci účtů.

    uživatel má možnost registrovat pouze tři účty.

    @param request: request klienta

    @var:   form: Formulář pro registraci
    @var:   message: pole s chybami
    @var:   accounts: uživatelovy již vytvořené účty

    @return: render html stránky s formulářem registrace a výpisem jednotlivých registrací
    """
    form = RegisterForm(request.POST or None, request.FILES or None)
    message = []
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            # message = register_form_check(form, request.user)
            if len(message) == 0:
                form.save()

    accounts = UserAccount.objects.filter(user=request.user)
    return render(request, 'projects/accounts_register.html', {
        'form': form,
        'accounts': accounts,
        'message': message,
    })

@login_required(login_url='/accounts/login/')
def register_form_check(form: RegisterForm, user: User) -> list:
    """ Funkce hledá chyby v registračním formuláři

    Kontroluje se jestli existuje účet se stejným jménem,
    počet vytvořených účtů (max 3),
    jestli uživatel vyplnil pole pro heslo
    a jestli se hesla shodují.

    @param form: registrační formulář
    @param user: uživatel, který formulář vyplnil

    @var    users: účty, které uživatel vytvořil
    @var    message: list pro chyby
    @var    acc: jeden účet pro kontrolu uživatelského jména
    @return: list: s chybami nebo prázdný list
    """
    users = UserAccount.objects.filter(user=user)
    message = []
    if users.exists():
        acc = UserAccount.objects.filter(jmeno=form.instance.jmeno, user=user)
        if acc.exists():
            message.append('Tento uživatel již existuje')
        if users.count() >= 3:
            message.append('Už jsi založil tři uživatele')
    if form.instance.heslo.strip() == '':
        message.append('Prázdné heslo')
    if not form.instance.heslo == form.instance.heslo_znovu:
        message.append('Hesla se neshodují')
    return message

@login_required(login_url='/accounts/login/')
def login_form_check(form: LoginForm) -> bool:
    """Funkce pro přihlášení se do účtu.

    Funkce se podívá do databáze, jestli existuje účet, který uživatel založil, kontroluje se
    název účtu a heslo.

    @param form: přihlašovací formulář


    @var accout: účet vytvořený uživatelem
    @return:    1. True pokud přihlášení proběhlo
                2. False pokud ne
    """
    account = UserAccount.objects.filter(jmeno=form.data.get('jmeno'),
                                         heslo=form.data.get('heslo'))

    if account.exists():
        return False
    return True

@login_required(login_url='/accounts/login/')
def done_view(request):
    """View Pro projekt "Accounts"

    Pokud se uživateli podaří se přihlásit do účtu který sám vytvořil, bude
    sem přesměrován a je mu zobrazena správa o úspěšném přihlášení.

    @return render html stránky s textem že přihlášení proběhlo v pořádku"""
    return render(request, 'projects/done.html')
