from django.urls import path, include
from . import views
from .models import Users
urlpatterns = [
    path('', views.MyListView.as_view(), name='list'),
    path('get_users/', views.getFollowers, name='users'),
    path('myretweet/', views.retweetMytweet, name='myretweet'),
    path('arrange_follow/', views.arrangeFollow, name='arrange_follow'),
    path('refavorite/', views.refavorite, name='refavorite'),
    path('favorite/', views.refavorite, name='favorite'),
]
