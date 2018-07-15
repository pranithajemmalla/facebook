from django.urls import path
from django.contrib.auth import views
from facebook.Views import userview
# app_name="fb"
urlpatterns = [
    path(r'',views.login,{'template_name':'fb/login.html'},name='login'),
    path(r'login/', views.login, {'template_name': 'fb/login.html'}, name="login"),
    path(r'logout/', views.logout, {'template_name': 'fb/login.html'}, name="logout"),
    path(r'register/',userview.register,name="register"),
    path(r'home/',userview.home,name='home'),
    path(r'updateprofile/<int:pk>',userview.Updateprofile.as_view(),name="updateprofile"),
    path(r'addpost/<int:posts_id>',userview.Addpost.as_view(),name="addpost"),
    path(r'requestfriend/',userview.RequestFriend,name="requestfriend"),
    path(r'likepost/', userview.likePost, name='likepost'),
    path(r'acceptrequest/',userview.AcceptFriend,name='acceptrequest'),
    path(r'addcomment',userview.AddComment,name='addcomment'),
    path(r'messages',userview.viewmessages,name='viewmessages'),
    path(r'sendmessage',userview.SendMessage,name='sendmessage'),
    path(r'requests',userview.getRequests,name="requests"),
    path(r'api/search/',userview.SearchUser,name="search"),
    path(r'view_profile/<int:id>',userview.ViewProfile,name="viewprofile"),
    path(r'updatepost/<int:pk>',userview.UpdatePost.as_view(),name="postupdate"),
    path(r'deletepost',userview.DeletePost,name="deletepost")
]
