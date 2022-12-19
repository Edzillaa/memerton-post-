from django.contrib import admin
from .models import Meme, Comment

# Register your models here.
admin.site.register(Meme)
admin.site.register(Comment)