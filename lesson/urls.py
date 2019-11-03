from django.urls import path
from . import views

urlpatterns = [
    path("lessons/explore/", views.lesson_explore, name="lesson_explore"),
    path("lessons/", views.get_queryset, name="search_results"),
    path("lessons/about/", views.lesson_about, name="lesson_about"),
	path("lessons/faq/", views.lesson_faq, name="lesson_faq"),
    path("", views.lesson_index, name="lesson_index"),
    path("lessons/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<int:pk>/edit/", views.lesson_edit, name="lesson_edit"),
    path("tags/<tag>/", views.lesson_tag, name="lesson_tag"),
    path("lessons/new/", views.lesson_new, name="lesson_new"),
    path("lessons/<int:pk>/delete",views.lesson_delete,name="lesson_delete"),
    path("lessons/results",views.lesson_search,name="lesson_search"),
	path("dashboard",views.lesson_dashboard,name="lesson_dashboard"),
    #path("curriculum/new/", views.curriculum_new, name="curriculum_new"),
]