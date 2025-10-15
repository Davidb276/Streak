from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("users/", include("users.urls")),
    path("vacancies/", TemplateView.as_view(template_name="vacancies/vacancy_list.html"), name="vacancies"),
    path("challenges/", TemplateView.as_view(template_name="challenges/challenge_list.html"), name="challenges"),
]
