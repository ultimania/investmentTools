from django.urls import path, include
from . import views
from .models import Users
urlpatterns = [
    path('', views.MyListView.as_view(), name='list'),
    path('get_users/', views.getFollowers, name='users'),
    path('myretweet/', views.retweetMytweet, name='myretweet'),
]
