from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import PIL
from django.utils import timezone
import datetime
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='documents/',null=True,blank=True,default='documents/default.jpg')
    DOB=models.DateField(null=True,blank=True)
    city=models.CharField(max_length=128,null=True,blank=True)
    phone=models.CharField(max_length=128,null=True,blank=True)
    Gender=models.CharField(max_length=128,null=True,blank=True)
    College=models.CharField(max_length=128,null=True,blank=True)
    School=models.CharField(max_length=128,null=True,blank=True)

    def __str__(self):
        return self.College

    def create_profile(sender,**kwargs):
        if kwargs['created']:
            user_profile=Profile.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile,sender=User)

class Friend(models.Model):
    user_id=models.IntegerField()
    users=models.ManyToManyField(User)

class Post(models.Model):
    title=models.CharField(max_length=128)
    image=models.ImageField(upload_to='documents/',null=True,blank=True)
    video=models.URLField(null=True,blank=True)
    date_created= models.DateTimeField(default=timezone.now().replace(microsecond=0))
    def __str__(self):
        return self.title
    posts=models.ForeignKey(User,on_delete=models.CASCADE)

class FriendRequests(models.Model):
    uid=models.IntegerField()
    fid=models.IntegerField()

class Like(models.Model):
    postId=models.IntegerField()
    UserId=models.IntegerField()

class Comment(models.Model):
    postId=models.IntegerField()
    UserId=models.IntegerField()
    comment=models.CharField(max_length=128)

class Message(models.Model):
    fid=models.IntegerField()
    message=models.CharField(max_length=300)
    time=models.DateTimeField()