from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import LessonForm
from .functions import form_validate_and_save
from .models import Lesson
import logging

logger = logging.getLogger(__name__)


def lesson_index(request):
    Lessons = Lesson.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
        "current": 'index',
    }
    return render(request, "lesson_index.html", context)

def lesson_explore(request):
    Lessons = Lesson.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
        "current": 'explore',
    }
    current = 'explore'
    print(current)
    return render(request, "lesson_explore.html", context)

def lesson_tag(request, tag):
    lessons = Lesson.objects.filter(
        tags__name__contains=tag
    ).order_by(
        '-created_on'
    )
    context = {
        "tag": tag,
        "lessons": lessons,
        "current":'tag',
    }
    current = 'tag'
    return render(request, "lesson_tag.html", context)


def lesson_detail(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    # comments = Comment.objects.filter(lesson=lesson)
    context = {
        "lesson": lesson,
        # "comments": comments,
        "current":'detail',

    }
    return render(request, "lesson_detail.html", context)


def lesson_new(request):
    context = {
        "pk": 0,
        "form": LessonForm()
    }
    return render(request, "lesson_edit.html", context)

def lesson_delete(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    lesson.delete()
    
    return redirect('lesson_index')

def lesson_edit(request, pk):
    if pk > 0:
        lesson = Lesson.objects.get(pk=pk)
    else:
        lesson = None

    if request.method == "POST":
        if pk > 0:
            form = LessonForm(request.POST, instance=lesson)
        else:
            form = LessonForm(request.POST)
        lesson = form_validate_and_save(form, request)
        if lesson:
            return redirect('lesson_detail', pk=lesson.pk)
        else:
            logger.error("lesson_edit form invalid: {}".format(form.errors))

    context = {
        "pk": pk,
        "form": LessonForm(instance=lesson) if pk > 0 else LessonForm()
    }
    return render(request, "lesson_edit.html", context)
