from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Task, Tag
from django.http import Http404
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator
from datetime import datetime


# Create your views here.

def home(request):
    all_tasks = Task.objects.all().order_by("?")
    for task in all_tasks:
        if task.due_date < datetime.now().date():
            Task.objects.filter(id=task.id).update(status="finished")

    context = {"tasks": all_tasks}
    return render(request, "home.html", context=context)


def task_filter(sorting_method, filter_method=None):
    if filter_method:
        all_tasks = Task.objects.filter(status=filter_method)
    else:
        all_tasks = Task.objects.all()
    if not sorting_method:
        all_tasks = all_tasks.order_by('due_date')
    elif sorting_method == 'Title_ASC':
        all_tasks = all_tasks.order_by('title')
    elif sorting_method == 'Title_DESC':
        all_tasks = all_tasks.order_by('-title')
    elif sorting_method == 'Date_ASC':
        all_tasks = all_tasks.order_by('due_date')
    elif sorting_method == 'Date_DESC':
        all_tasks = all_tasks.order_by('-due_date')
    return all_tasks


def tasks(request):
    try:
        filter_method = request.GET.get('gridRadios')
        sorting_method = request.GET.get('select')
        print(filter_method)
        if not filter_method:
            all_tasks = task_filter(sorting_method)

        elif filter_method == "finished":

            all_tasks = task_filter(sorting_method, filter_method)

        elif filter_method == "ongoing":

            all_tasks = task_filter(sorting_method, filter_method)

        paginator = Paginator(all_tasks, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"tasks": page_obj}
        return render(request, "tasks.html", context=context)
    except:
        return redirect('tasks')


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
        searched = request.GET.get('searched')
        if searched:
            # results = list(set(chain(Task.objects.filter(title__icontains=searched),
            #                          Task.objects.filter(description__icontains=searched),
            #                          Task.objects.filter(tag__name__icontains=searched)
            #                          )
            #                    )
            #                )
            results = Task.objects.filter(Q(title__icontains=searched)
                                          | Q(description__icontains=searched)
                                          | Q(tag__name__icontains=searched)
                                          ).distinct()
            paginator = Paginator(results, 2)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(request, 'search_result.html', {"searched": searched, "results": page_obj})
        else:
            return render(request, 'search_result.html', {"searched": searched})


def category(request):
    all_categories = Category.objects.all()

    paginator = Paginator(all_categories, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"categories": page_obj}

    return render(request, "category.html", context=context)


def category_task(request, pk):
    category_item = get_object_or_404(Category, id=pk)
    all_tasks = Task.objects.filter(category=category_item)

    paginator = Paginator(all_tasks, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"tasks": page_obj}
    return render(request, "category_task.html", context=context)
