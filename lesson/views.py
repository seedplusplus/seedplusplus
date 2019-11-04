from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import HttpResponse 
from django.core.files.storage import FileSystemStorage

from .forms import *
from .functions import form_validate_and_save, has_perm, set_perm
from .models import Lesson,Curriculum,UserProfile
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
    #Curricula = Curriculum.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
        #"Curricula": Curricula,
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

def lesson_faq(request):
    Lessons = Lesson.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
        "current": 'faq',
    }
    return render(request, "lesson_faq.html", context)

@login_required
def lesson_dashboard(request):
    Lessons = Lesson.objects.all().order_by('-created_on')
    Curricula = Curriculum.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
        "Curricula": Curricula,
        "current": 'dashboard',
    }
    return render(request, "lesson_dashboard.html", context)

@login_required
def upload_prof_pic(request):
    context = {"current": 'uploadPic'}
    return render(request, "upload_prof_pic.html", context)

@login_required
def prof_pic_view(request,username):
    if request.method == 'POST' and request.FILES['profpic']:
        profpic = request.FILES['profpic']
        fs = FileSystemStorage()
        filename = fs.save(profpic.name, profpic)
        upload = fs.url(filename)
        
        current_user, created = UserProfile.objects.get_or_create(user=request.user)
        current_user.profile_pic = upload
        current_user.save()
        return render(request, 'lesson_dashboard.html', {'profile_pic': upload})
        
    return render(request, 'lesson_dashboard.html', {'profile_pic': None})

#def success(request):
    #return HttpResponse('successfully uploaded')

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

def apply_filters(request, search_text=None):
    
    if search_text != None:
        Lessons = search_lessons(search_text)
    else:
        Lessons = Lesson.objects.all().order_by('-created_on')    
    
    length_filters = request.GET.getlist('length')
    language_filters = request.GET.getlist('language')
    difficulty_filters = request.GET.getlist('difficulty')
    
    length_map = {0 : "less-than-1",
                    1 : "1-hour",
                    2 : "2-hour"}
    
    difficulty_map = {0 : "beginner",
                    1 : "intermediate",
                    2 : "advanced"}
        
    # Filter duration    
    if len(length_filters) != 0:
        Lessons = [x for x in Lessons if length_map[min(2,int(x.length))] in length_filters]
    
    # Filter language
    if len(language_filters) != 0:
        Lessons = [x for x in Lessons if x.language in language_filters]
    
    # Filter difficulty
    if len(difficulty_filters) != 0:
        Lessons = [x for x in Lessons if x.difficulty in difficulty_filters]
    
    context = {
        "Lessons": Lessons,
        "current":'explore',
        "search_text": search_text
    }
    return render(request, "lesson_explore.html", context)

@login_required
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


@login_required
def lesson_delete(request, pk):
    lesson = Lesson.objects.get(pk=pk)

    if not has_perm(request.user, lesson, 'lesson.delete_lesson'):
        return redirect('/login/?next=%s' % request.path)

    lesson.delete()

    return redirect('lesson_index')

@login_required()
def curriculum_new(request):

    if request.method == "POST":
        form = CurriculumForm(request.POST)
        curriculum = form_validate_and_save(form, request)
        if curriculum:
            return redirect('curriculum_detail', pk=curriculum.pk)
        else:
            logger.error("curriculum_new form invalid: {}".format(form.errors))

    context = {
        "form": CurriculumForm(),
    }
    return render(request, "curriculum_new.html", context)

def curriculum_detail(request, pk):
    curriculum = Curriculum.objects.get(pk=pk)
    # comments = Comment.objects.filter(lesson=lesson)
    context = {
        "curriculum": curriculum,
        # "comments": comments,
        "current":'detail',

    }
    return render(request, "curriculum_detail.html", context)

def get_queryset(self): # new
    query = self.request.GET.get('q')
    return Lesson.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
