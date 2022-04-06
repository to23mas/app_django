from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UkolForm, RegisterForm, LoginForm
from .models import Ukol, Project, UserAccount


def hello_view(request):
    return HttpResponse('Hello, world.')


def todo_view(request):
    form = UkolForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.instance.user = request.user
        form.save()

    ukoly = Ukol.objects.filter(user=request.user)
    return render(request, 'projects/todo.html', {'form': form,
                                                  'ukoly': ukoly})


def todo_two_view(request):
    form = UkolForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.instance.user = request.user

        form.save()
        return redirect('projects:todo_two')

    ukoly = Ukol.objects.filter(user=request.user)
    return render(request, 'projects/todo_two.html', {'form': form,
                                                      'ukoly': ukoly})


def delete_todo(request, todo_id: int):
    Ukol.objects.get(id=todo_id).delete()
    return redirect('projects:todo_two')


def all_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/all.html', {'projects': projects})


def cross_view(request):
    return render(request, 'projects/cross.html')


def accounts_login_one(request):
    form = LoginForm(request.POST or None, request.FILES or None)
    fail = ''
    if request.method == 'POST':
        if login_form_check(form, request.user):
            fail = 'chybné heslo nebo jméno'
        else:
            return redirect('projects:done')

    users = UserAccount.objects.filter(user=request.user)
    return render(request, 'projects/account_login.html', {'form': form,
                                                           'fail': fail,
                                                           'users': users, })


def accounts_register_view(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    message = []
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            message = register_form_check(form, request.user)
            if len(message) == 0:
                form.save()

    accounts = UserAccount.objects.filter(user=request.user)
    return render(request, 'projects/accounts_register.html', {
        'form': form,
        'accounts': accounts,
        'message': message,
    })


def register_form_check(form: RegisterForm, user: User) -> list:
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

def login_form_check(form: LoginForm, user: User) -> bool:
    account = UserAccount.objects.filter(jmeno=form.instance.jmeno,
                                         heslo=form.instance.heslo,
                                         user=user)

    if account.exists():
        return False
    return True

def done_view(request):
    return render(request, 'projects/done.html')
