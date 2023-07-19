from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Task, Tag
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import mimetypes
from django.http.response import HttpResponse, FileResponse
import os
from django.conf import settings


# Create your views here.

def home(request):
    if request.method == "GET":
        all_tasks = Task.objects.all().order_by("?")
        for task in all_tasks:
            if task.due_date < datetime.now().date():
                Task.objects.filter(id=task.id).update(status="done")
        all_tasks = Task.objects.all().order_by("?")
        context = {"tasks": all_tasks}
        return render(request, "home.html", context=context)


def task_filter(sorting_method, filter_method=None):
    if filter_method is None or filter_method == "all":
        all_tasks = Task.objects.all()

    else:
        all_tasks = Task.objects.filter(status=filter_method)

    if sorting_method == 'Title_ASC':
        all_tasks = all_tasks.order_by('title')
    elif sorting_method == 'Title_DESC':
        all_tasks = all_tasks.order_by('-title')
    elif sorting_method == 'Date_ASC':
        all_tasks = all_tasks.order_by('due_date')
    elif sorting_method == 'Date_DESC':
        all_tasks = all_tasks.order_by('-due_date')
    elif sorting_method == 'No Order':
        all_tasks = all_tasks
    else:
        all_tasks = all_tasks.order_by('due_date')
    return all_tasks


def tasks(request):
    if request.method == "GET":
        try:
            filter_method = request.GET.get('gridRadios')
            sorting_method = request.GET.get('select')

            if filter_method == "all":
                all_tasks = task_filter(sorting_method, filter_method)

            elif filter_method == "done":
                all_tasks = task_filter(sorting_method, filter_method)

            elif filter_method == "doing":
                all_tasks = task_filter(sorting_method, filter_method)

            elif filter_method == "todo":
                all_tasks = task_filter(sorting_method, filter_method)

            else:
                all_tasks = task_filter(sorting_method)

            paginator = Paginator(all_tasks, 3)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context = {"tasks": page_obj}
            return render(request, "tasks.html", context=context)
        except:
            raise Http404("No matches the given query.")


def task_details(request, pk):
    if request.method == "GET":
        try:
            task = get_object_or_404(Task, id=pk)
            context = {"task": task, "name": os.path.basename(f"{task.file}")}
            return render(request, "task_details.html", context=context)
        except:
            raise Http404("No matches the given query.")


def search(request):
    if request.method == "GET":
        return render(request, 'search.html')


def search_result(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        if searched:

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
    if request.method == "GET":
        all_categories = Category.objects.all()
        paginator = Paginator(all_categories, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"categories": page_obj}

        return render(request, "category.html", context=context)


def category_task(request, pk):
    if request.method == "GET":
        category_item = get_object_or_404(Category, id=pk)
        all_tasks = Task.objects.filter(category=category_item)

        paginator = Paginator(all_tasks, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"tasks": page_obj}
        return render(request, "category_task.html", context=context)


def about_us(request):
    return render(request, "about_us.html")


def download_file(request, filename):
    filepath = settings.BASE_DIR / f'media/uploads/{filename}'
    file = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = FileResponse(file, content_type=mime_type)
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response


# def view_file(request, filename):
#     print("hiiii")
#     filepath = settings.BASE_DIR / f'media/uploads/{filename}'
#     #
#     mime_type, _ = mimetypes.guess_type(filepath)
#     with open(filepath, 'rb') as file:
#         response = HttpResponse(file.read(), content_type=mime_type)
#         response['Content-Disposition'] = f"Inline; filename='{filename}'"
#     # return render(request, "show.html",context={"data":filepath})
#     return response
