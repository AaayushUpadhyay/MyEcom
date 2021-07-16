from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import secrets
import string
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(default="default.jpg",upload_to="profile_pics")
    
    def __str__(self):
        return self.user.username


class Token(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=10)

    def token_create(self):
        token=''.join([secrets.choice(self.user.username+'0123456789') for i in range(10)])
        self.token=token

    def __str__(self):
        return self.user.username+"'s token"