from django.urls import path
from . import views

urlpatterns = [
    path("", views.lesson_index, name="lesson_index"),
    path("lessons/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<int:pk>/edit/", views.lesson_edit, name="lesson_edit"),
    path("tags/<tag>/", views.lesson_tag, name="lesson_tag"),
    path("lessons/new/", views.lesson_new, name="lesson_new"),
    path("lessons/<int:pk>/delete",views.lesson_delete,name="lesson_delete")
]