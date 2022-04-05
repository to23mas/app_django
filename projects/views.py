from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UkolForm
from .models import Ukol, Project

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
