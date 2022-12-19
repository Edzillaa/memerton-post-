from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
import boto3
from .models import Meme, Comment
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'eaga-catcollector'

def home(request):
    # memes = Meme.objects.all() #pulling all memes from our db
    return render(request, 'home.html')

def create(request):
    return render(request, 'memes/create.html')


def add_photo(request):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # photo = Meme(url=url)
            # photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('meme_create')

def add_meme(request):
    
    return redirect('home')

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

