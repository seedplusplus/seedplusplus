from django.shortcuts import render
from lesson.models import Lesson


def lesson_index(request):
    Lessons = Lesson.objects.all().order_by('-created_on')
    context = {
        "Lessons": Lessons,
    }
    return render(request, "lesson_index.html", context)


def lesson_tag(request, tag):
    lessons = Lesson.objects.filter(
        categories__name__contains=tag
    ).order_by(
        '-created_on'
    )
    context = {
        "tag": tag,
        "lessons": lessons
    }
    return render(request, "lesson_tag.html", context)

def lesson_detail(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    # comments = Comment.objects.filter(lesson=lesson)
    context = {
        "lesson": lesson,
        # "comments": comments,
    }

    return render(request, "lesson_detail.html", context)
