from django.urls import path
from . import views

urlpatterns = [
    #general views
    path('', views.home, name='home'),
    path('create/<photo>/', views.create, name='meme_create'),
    path('memes/<int:meme_id>', views.meme_details, name='meme_details'),
    #Meme
    path('memes/add_photo/', views.add_photo, name='add_photo'),
    path('memes/add_meme/<photo>/', views.add_meme, name = 'add_meme'),
    path('memes/add_like/', views.add_like, name="add_like"),
    path('memes/add_dislike/', views.add_dislike, name="add_dislike"),
    path('memes/<int:meme_id>/delete/', views.delete_meme, name='delete_meme'),
    path('memes/my_memes/', views.sort_my_memes, name='sort_my_memes'),
    path('memes/liked/', views.sort_liked, name='sort_liked'),
    path('memes/hated/', views.sort_hated, name='sort_hated'),
    #Comment
    path('memes/<int:meme_id>/comments', views.add_comment, name="add_comment"),
    path('memes/<int:meme_id>/comments/<int:comment_id>/delete', views.delete_comment, name="delete_comment"),
    #sign_up
    path('accounts/signup/', views.signup, name='signup')
]