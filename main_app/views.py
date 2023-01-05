from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
import boto3
from .models import Meme, Comment, User
from math import sqrt
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime as date
import base64
import io

S3_BASE_URL = 'https://s3.us-west-2.amazonaws.com/'
BUCKET = 'memertonpost'

def home(request):
    memes = Meme.objects.all() #pulling all memes from our db
    return render(request, 'index.html', {'memes': memes})

@login_required
def create(request, photo=" "):
    #passing photo name via route:
    if photo != " ":
        url = f"{S3_BASE_URL}{BUCKET}/{photo}"
    else:
        url = " "
    #passing photo_name to create_page. this will be important when we want to save meme.
    return render(request, 'memes/create.html', {"url": url, "photo_name": photo})

def meme_details(request, meme_id):
    meme = Meme.objects.get(id=meme_id)
    comments = Comment.objects.filter(meme=meme_id).order_by('-id')
    comment_list = []
    for comment in comments:
        opinion = {}
        opinion['user'] = User.objects.get(id=comment.user.id).username
        opinion['id']= comment.id
        opinion['comment']= comment.comment
        opinion['date'] = comment.date
        comment_list.append(opinion)
    return render(request, 'memes/details.html', {'meme': meme, 'comments': comment_list} )

@login_required
def add_photo(request):
    photo_file = request.FILES.get('photo-file', None) #this saves uploaded photo name
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        # except:
        #     print('An error occured uploading file to S3')
    return redirect('meme_create', key)

@login_required
def add_meme(request, photo):
    key = photo
    raw_data= request.POST.get('photo-file')[request.POST.get('photo-file').find(',')+1:]
    b = base64.b64decode(raw_data)
    # print(b)
    # img = Image.open(io.BytesIO(b))
    # img.convert('RGB')
    # img.show()
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(io.BytesIO(b), BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        meme = Meme.objects.create(url=url, likes = 0, dislikes = 0, name=request.POST.get('meme-name'), user=request.user)
        meme.save()
    except:
        print('An error occured uploading meme to S3')
    return redirect('home')

@login_required
def delete_meme(request, meme_id):
    Meme.objects.get(id=meme_id).delete()
    return redirect('home')

@login_required
def add_comment(request, meme_id):
    meme = Meme.objects.get(id=meme_id)
    newComment = Comment.objects.create(comment=request.POST.get('comment'), user=request.user, meme=meme, date=date.now() )
    newComment.save()
    return redirect('meme_details', meme_id)

@login_required
def delete_comment(request, meme_id, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect('meme_details', meme_id)

@login_required
def add_like(request):
    meme = Meme.objects.get(id=request.POST.get('meme-id'))
    meme.likes += 1
    meme.confidence = confidence(meme.likes, meme.dislikes)
    meme.save()
    return redirect('home')

@login_required
def add_dislike(request):
    meme = Meme.objects.get(id=request.POST.get('meme-id'))
    meme.dislikes += 1
    meme.confidence = confidence(meme.likes, meme.dislikes)
    meme.save()
    return redirect('home')

def _confidence(likes, dislikes):
    n = likes + dislikes
    if n == 0:
        return 0
    z = 1.281551565545
    p = float(dislikes) / n
    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z
    return (left - right) / under

def confidence(likes, dislikes):
    if likes + dislikes == 0:
        return 0
    else:
        return _confidence(likes, dislikes)

def sort_my_memes(request):
    my_memes = Meme.objects.filter(user=request.user).order_by('-confidence')
    return render(request, 'index.html', {'memes': my_memes})

def sort_hated(request):
    return redirect('home')

def sort_liked(request):
    liked_memes = Meme.objects.all().order_by('confidence')
    return render(request, 'index.html', {'memes': liked_memes})

def signup(request):
  error_message = ''
  if request.method == 'POST': 
    form = UserCreationForm(request.POST) 
    if form.is_valid():
      user = form.save()
      login(request,user)
      return redirect('home')
    else:
      print(form.errors)
      error_message=form.errors
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message }
  return render(request, 'registration/signup.html', {'form': form, 'error_message': error_message})

