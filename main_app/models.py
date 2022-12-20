from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User

class Meme(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    #if we have time: create new model for likes and dislikes, restricting # of times user can like or dislike a meme.
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    def __str__(self):
        return f"Photo for user_id:{self.url} for meme: {self.name}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    date = models.DateField('comment date')
    comment = models.TextField(max_length=250)

    class Meta:
        ordering = ['-date']

#if we have time: Message model for live chat.


