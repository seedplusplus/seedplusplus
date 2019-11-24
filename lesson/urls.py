from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path("lessons/explore/", views.lesson_explore, name="lesson_explore"),
    path("lessons/", views.get_queryset, name="search_results"),
    path("lessons/about/", views.lesson_about, name="lesson_about"),
    path("", views.lesson_index, name="lesson_index"),
    path("lessons/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("lessons/<int:pk>/edit/", views.lesson_edit, name="lesson_edit"),
    path("tags/<tag>/", views.lesson_tag, name="lesson_tag"),
    path("lessons/new/", views.lesson_new, name="lesson_new"),
    path("lessons/<int:pk>/delete",views.lesson_delete,name="lesson_delete"),
    path("lessons/explore/results",views.lesson_search,name="lesson_search"),
    path("lessons/faq/", views.lesson_faq, name="lesson_faq"),
    path("curriculum/new/", views.curriculum_new, name="curriculum_new"),
    path("curriculum/<int:pk>/", views.curriculum_detail, name="curriculum_detail"),
    path("dashboard",views.lesson_dashboard, name="lesson_dashboard"),
    path("lessons/filters/<search_text>",views.apply_filters, name="apply_filters"),
    path("lessons/filters/",views.apply_filters, name="apply_filters"),
    path("upload_prof_pic",views.upload_prof_pic, name="upload_prof_pic"),
    path("image_upload/<username>", views.prof_pic_view, name="image_upload"), 
   ]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)