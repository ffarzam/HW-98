from django.shortcuts import render, get_object_or_404
from .models import Category, Task, Tag
from django.http import Http404
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator


# Create your views here.

def home(request):
    all_tasks = Task.objects.all()
    context = {"tasks": all_tasks}
    return render(request, "home.html", context=context)


def tasks(request):
    all_tasks = Task.objects.all().order_by("due_date")

    paginator = Paginator(all_tasks, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"tasks": page_obj}
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
