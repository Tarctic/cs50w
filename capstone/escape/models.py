from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings

class User(AbstractUser):
    pass

class Profile(models.Model):
    gamer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_user")
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"User {self.id}:{self.gamer}"

