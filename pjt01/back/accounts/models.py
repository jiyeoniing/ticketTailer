from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    nickname = models.CharField(max_length=30,unique=True)
    username = models.CharField(max_length=150,unique=True )
    password = models.CharField(max_length=200)
    profile_img = models.ImageField(blank=True, upload_to='accounts/')
    created_at = models.DateTimeField(auto_now_add=True)