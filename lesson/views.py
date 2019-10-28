from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .forms import LessonForm
from .functions import form_validate_and_save, has_perm, set_perm
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
    #print(current)
    return render(request, "lesson_explore.html", context)

def lesson_about(request):
    Lessons = Lesson.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
        "current": 'about',
    }
    return render(request, "lesson_about.html", context)

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

def lesson_search(request):
    
    query = SearchQuery(request.GET.get('home_search'))
    vector = SearchVector('title','description','body','language','difficulty','tags','length')
    weights_ = [1.0,0.4,0.2,1.0,0.1,1.0,0.1]
    results = Lesson.objects.annotate(rank=SearchRank(vector,query,weights=weights_)).filter(rank__gte=0.01).order_by('-rank')
    
    # Remove duplicates
    results = list( dict.fromkeys(results) )
        
    context = {
        "Lessons": results,
        "current":'search',
    }
    return render(request, "lesson_explore.html", context)

@login_required()
def lesson_new(request):

    if request.method == "POST":
        form = LessonForm(request.POST)
        lesson = form_validate_and_save(form, request)
        if lesson:
            return redirect('lesson_detail', pk=lesson.pk)
        else:
            logger.error("lesson_new form invalid: {}".format(form.errors))

    context = {
        "form": LessonForm(),
    }
    return render(request, "lesson_new.html", context)

@login_required
def lesson_edit(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    if not has_perm(request.user, lesson, 'lesson.change_lesson'):
        return redirect('/login/?next=%s' % request.path)
    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        lesson = form_validate_and_save(form, request, edit=True)

        if lesson:
            return redirect('lesson_detail', pk=lesson.pk)
        else:
            logger.error("lesson_edit form invalid: {}".format(form.errors))
    else:
        context = {
            "pk": pk,
            "form": LessonForm(instance=lesson)
        }
        return render(request, "lesson_edit.html", context)

def lesson_delete(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    lesson.delete()

    return redirect('lesson_index')

def get_queryset(self): # new
    query = self.request.GET.get('q')
    return Lesson.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
