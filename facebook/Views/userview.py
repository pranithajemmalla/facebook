from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.shortcuts import redirect,render
from django import forms
from rest_framework import generics
from django.views import View
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.forms import ModelForm
from django import forms
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import datetime as dt
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from rest_framework import serializers
from PIL import Image

from facebook.models import *
class Registrationform(UserCreationForm):
    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
    def save(self,commit=True):
        user=super(Registrationform,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

def register(request):
    if request.method=='POST':
        form=Registrationform(request.POST)
        # import ipdb
        # ipdb.set_trace()
        if form.is_valid():
            form.save()
            userid=User.objects.values('id').latest('id')
            f=Friend(user_id=userid['id'],id=userid['id'])
            f.save()
            return redirect('login')
        else:
            return redirect('register')
    else:
        form=Registrationform()
        args={'form':form}
        return render(request,'fb/Register.html',args)

def home(request):
    # import ipdb
    # ipdb.set_trace()
    # Get friend requests of the user
    fr = FriendRequests.objects.filter(fid=request.user.id)
    frdreq=User.objects.filter(id__in=[f.uid for f in fr]).exclude(id=request.user.id)

    #Get requested users
    frbyuser=FriendRequests.objects.filter(uid=request.user.id)
    frdrequser = User.objects.filter(id__in=[f.fid for f in frbyuser])

    # Get friends of the user
    f=Friend.objects.get(user_id=request.user.id)
    frnds=f.users.all()

    # Get posts by the user and his friends
    posts = Post.objects.all().filter(Q(posts_id__in=[f.id for f in frnds])|Q(posts_id=f.id)).order_by('-date_created')
    pc=[]
    for p in posts:
        c=Comment.objects.filter(postId=p.id)
        likecnt=Like.objects.filter(postId=p.id).count()
        post_user_id=Post.objects.values('posts_id').get(id=p.id)
        post_username=User.objects.values('username').get( id=post_user_id['posts_id'])
        post_user_profilephoto=Profile.objects.values('profile_picture').get(user_id=post_user_id['posts_id'])
        date=Post.objects.values('date_created').get(id=p.id)
        pc.append({'p':p,'c':c,'likecnt':likecnt,'postusername':post_username,'postuserprofile':post_user_profilephoto,'postdate':date})

    # Get the suggestions list by excluding his friends
    users=User.objects.all().exclude(id=f.id).exclude(id__in=[f.id for f in frnds]).exclude(id__in=[f.uid for f in fr]).exclude(id__in=[f.id for f in frdrequser])

    # Get the post ids of the posts which user liked
    like=Like.objects.values('postId').filter(UserId=request.user.id)

    # Convert Queryset into list
    likelis=[]
    for likeobj in like:
        likelis.append(likeobj['postId'])
    # Context
    args={'posts':pc,'users':users,'frnds':frnds,'like':likelis,'fr':frdreq}

    return render(request,'fb/home.html',args)

class Addprofile(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['id','user']


class Updateprofile(UpdateView):
    model=Profile
    template_name = 'fb/add_profile.html'
    form_class = Addprofile
    success_url = reverse_lazy('home')

class Postform(forms.ModelForm):
    class Meta:
        model=Post
        exclude=['id','user_id','posts_id','posts','date_created']

class UpdatePost(UpdateView):
    model=Post
    template_name = 'fb/addpost.html'
    form_class = Postform
    success_url = reverse_lazy('home')

class Addpost(CreateView):
    template_name = "fb/addpost.html"
    form_class=Postform
    model = Post
    def get_context_data(self, **kwargs):
        context = super(Addpost, self).get_context_data(**kwargs)
        context.update({
            'postform': context.get('form'),
            'user_permissions': self.request.user.get_all_permissions()
        })
        return context
    def post(self, request, *args, **kwargs):
        posts = get_object_or_404(User, pk=kwargs.get('posts_id'))
        userform = Postform(request.POST,request.FILES)
        #userform.fields['date_created']=kwargs.get('posts_id')
        # import ipdb
        # ipdb.set_trace()
        if userform.is_valid():
            card = userform.save(commit=False)
            card.posts = posts
            card.date_created=timezone.now()
            card.save()
        return redirect('/home/')

def AcceptFriend(request):
    if request.method=="GET":
        fid = request.GET['friend_id']
        user=User.objects.get(id=fid)
        f1=Friend.objects.get(user_id=request.user.id)
        f2=Friend.objects.get(user_id=fid)
        f1.users.add(user)
        f2.users.add(request.user)
        f1.save()
        f2.save()
        FriendRequests.objects.filter(uid=request.user.id,fid=fid).delete()
        FriendRequests.objects.filter(uid=fid,fid=request.user.id).delete()
        return HttpResponse("Success!")
    else:
        return HttpResponse("Failed!")

def RequestFriend(request):
    if request.method=="GET":
        # import ipdb
        # ipdb.set_trace()
        fid = request.GET['friend_id']
        fr=FriendRequests(fid=fid,uid=request.user.id)
        fr.save()
        return HttpResponse("Success!")
    else:
        return HttpResponse("Failed!")

def likePost(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']

        if not Like.objects.filter(postId=post_id,UserId=request.user.id).exists():
            like=Like(postId=post_id,UserId=request.user.id)
            like.save()
        else:
            Like.objects.filter(postId=post_id,UserId=request.user.id).delete()
        likecnt=Like.objects.filter(postId=post_id).count()
        return HttpResponse(likecnt)
    else:
        return HttpResponse("0")

def AddComment(request):
    if request.method=="GET":
        post_id = request.GET['post_id']
        comment=request.GET['comment']
        cmt=Comment(postId=post_id,UserId=request.user.id,comment=comment)
        cmt.save()
        return HttpResponse('Success!!')
    else:
        return HttpResponse("Failed!!")

def viewmessages(request):
    return render(request,'fb/messages.html')

def SendMessage(request):
    pass

def getRequests(request):
    # Get friend requests of the user
    fr = FriendRequests.objects.filter(fid=request.user.id)
    frdreq = User.objects.filter(id__in=[f.uid for f in fr]).exclude(id=request.user.id)

    # Get requested users
    frbyuser = FriendRequests.objects.filter(uid=request.user.id)
    frdrequser = User.objects.filter(id__in=[f.fid for f in frbyuser])

    # Get friends of the user
    f = Friend.objects.get(user_id=request.user.id)
    frnds = f.users.all()
    users=User.objects.all().exclude(id=f.id).exclude(id__in=[f.id for f in frnds]).exclude(id__in=[f.uid for f in fr]).exclude(id__in=[f.id for f in frdrequser])

    return render(request,'fb/friendrequests.html',{'frdreqs':frdreq,'frnds':frnds,'users':users})


class UserdataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username=serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('name', instance.name)
        instance.save()
        return instance

def SearchUser(request):
    if request.method == "GET":
        # import ipdb
        # ipdb.set_trace()
        users = User.objects.all().filter(username__icontains=request.GET['query'])
        serializers = UserdataSerializer(users, many=True)
        return JsonResponse(serializers.data, safe=False)

def ViewProfile(request,id):
    profile_info=Profile.objects.all().get(user_id=id)
    user=User.objects.all().get(id=id)
    posts=Post.objects.filter(posts_id=id)
    pc = []
    for p in posts:
        c = Comment.objects.filter(postId=p.id)
        likecnt = Like.objects.filter(postId=p.id).count()
        post_user_id = Post.objects.values('posts_id').get(id=p.id)
        post_username = User.objects.values('username').get(id=post_user_id['posts_id'])
        post_user_profilephoto = Profile.objects.values('profile_picture').get(user_id=post_user_id['posts_id'])
        date = Post.objects.values('date_created').get(id=p.id)
        pc.append({'p': p, 'c': c, 'likecnt': likecnt, 'postusername': post_username,
                   'postuserprofile': post_user_profilephoto, 'postdate': date})
    like = Like.objects.values('postId').filter(UserId=id)

    # Convert Queryset into list
    likelis = []
    for likeobj in like:
        likelis.append(likeobj['postId'])
    return render(request,'fb/View_profile.html',{'suser':user,'profile':profile_info,'posts':pc,'like':likelis})


def DeletePost(request):
    pid = request.GET['pid']
    Post.objects.filter(id=pid).delete()
    return HttpResponse("Success")


