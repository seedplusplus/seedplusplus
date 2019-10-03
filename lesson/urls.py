from django.urls import path
from . import views

urlpatterns = [
    path("", views.lesson_index, name="lesson_index"),
    path("<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("<category>/", views.lesson_tag, name="lesson_tag"),
]