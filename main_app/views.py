from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
import boto3
from .models import Meme, Comment

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'eaga-catcollector'

def home(request):
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
    return redirect('/')