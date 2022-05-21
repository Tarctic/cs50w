from typing import Match
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings


class User(AbstractUser):
    pass
    # username, email, password

class Person(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_name")
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    following = models.ManyToManyField(User,blank=True,related_name='person_following')
    followers = models.ManyToManyField(User,blank=True,related_name='person_followers')

class Post(models.Model):
    content = models.CharField(max_length=1000)
    img = models.URLField(null=True,blank=True,default=None)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner", null=True)
    creation = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,blank=True,related_name='post_likers')

    class Meta:
        ordering = ['-creation']

    def __str__(self):
        return f"{[{self.poster},{self.likes},{self.creation}]}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "poster": self.poster.username,
            "creation": self.creation.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.username for user in self.likes.all()],
            "img": self.img
        }