from django.urls import path
from . import views

app_name = "vacancies"

urlpatterns = [
    path("", views.vacancy_list, name="list"),
    path("create/", views.vacancy_create, name="create"),
    path("<int:pk>/edit/", views.vacancy_update, name="edit"),
    path("<int:pk>/delete/", views.vacancy_delete, name="delete"),
    path("<int:pk>/apply/", views.vacancy_apply, name="apply"),
]
