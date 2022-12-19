from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meme, Comment
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    # memes = Meme.objects.all() #pulling all memes from our db
    return render(request, 'home.html')

def create(request):
    return render(request, 'memes/create.html')

def signup(request):
  error_message = ''
  if request.method == 'POST': 
    form = UserCreationForm(request.POST) 
    if form.is_valid():
      user = form.save()
      login(request,user)
      return redirect('index')
    else:
      print(form.errors)
      error_message=form.errors

  #if it's a get request or it's a bad post...    
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message }
  return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})
