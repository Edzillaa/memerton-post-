from django.urls import path
from . import views

urlpatterns = [
    #general views
    path('', views.home, name='home'),
    path('create/', views.create, name='meme_create'),
]