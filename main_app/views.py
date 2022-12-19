from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Meme, Comment


def home(request):
    return render(request, 'home.html')

def create(request):
    return render(request, 'memes/create.html')