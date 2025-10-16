from django.urls import path
from . import views

app_name = "users" 

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("", views.user_list_view, name="user_list"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile")
]
