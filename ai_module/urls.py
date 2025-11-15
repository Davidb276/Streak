from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_view, name="chat"),
    path("generator/", views.generator_view, name="generator"),
    path("recommender/", views.recommender_view, name="recommender"),
]
