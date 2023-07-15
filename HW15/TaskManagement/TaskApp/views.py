from django.shortcuts import render, get_object_or_404
from .models import Category, Task, Tag
from django.http import Http404


# from django.http import Http404


# Create your views here.

def home(request):
    return render(request, "home.html")


def tasks(request):
    all_tasks = Task.objects.all()

    # print(all_tasks)
    for task in list(all_tasks):
        print(type(task.tag))
        print(task.tag)

    context = {"tasks": all_tasks}
    return render(request, "tasks.html", context=context)


def task_details(request, pk):
    try:
        task = get_object_or_404(Task, id=pk)
        context = {"task": task}
        return render(request, "task_details.html", context=context)
    except:
        raise Http404("No matches the given query.")
