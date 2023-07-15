from django.shortcuts import render, get_object_or_404
from .models import Category, Task, Tag
from django.http import Http404
from django.db.models import Q
from itertools import chain


# Create your views here.

def home(request):
    return render(request, "home.html")


def tasks(request):
    all_tasks = Task.objects.all()
    context = {"tasks": all_tasks}
    return render(request, "tasks.html", context=context)


def task_details(request, pk):
    try:
        task = get_object_or_404(Task, id=pk)
        context = {"task": task}
        return render(request, "task_details.html", context=context)
    except:
        raise Http404("No matches the given query.")


def search(request):
    return render(request, 'search.html')


def search_result(request):
    if request.method == "GET":
        # results = request.POST['searched']
        searched = request.GET.get('searched')

        results = list(chain(Task.objects.filter(title__icontains=searched),
                             Task.objects.filter(description__icontains=searched),
                             Task.objects.filter(tag__name__icontains=searched)
                             )
                       )
        # results = Task.objects.filter(Q(title__icontains=searched)
        #                               | Q(description__icontains=searched)
        #                               | Q(tag__name__icontains=searched)
        #                               )

    return render(request, 'search_result.html', {"searched": searched, "results": results})
