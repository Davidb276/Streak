# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    level = models.IntegerField(default=1)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
