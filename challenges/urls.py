from django.urls import path
from . import views

app_name = "challenges"

urlpatterns = [
    path('', views.retos_personalizados, name='challenge_list'),
    path("completar/<str:session_id>/", views.completar_reto, name="completar_reto"),
]
