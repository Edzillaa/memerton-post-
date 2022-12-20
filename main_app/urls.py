from django.urls import path
from . import views

urlpatterns = [
    #general views
    path('', views.home, name='home'),
    path('create/<photo>/', views.create, name='meme_create'),

    #Meme
    path('memes/add_photo/', views.add_photo, name='add_photo'),
    path('memes/add_meme/<photo>/', views.add_meme, name = 'add_meme'),
    path('memes/add_like/', views.add_like, name="add_like"),
    path('memes/add_dislike/', views.add_dislike, name="add_dislike"),

    #sign_up
    path('accounts/signup/', views.signup, name='signup')
]