from django.urls import path

from . import views

urlpatterns = [
	path("signup/", views.SignUp.as_view(), name="signup"),
        path("profile/", views.profile_page, name="profile"),
    path("delete/", views.delete_self, name="delete_self")
]