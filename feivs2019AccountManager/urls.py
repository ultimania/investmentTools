from django.urls import path, include
from . import views
from .models import Users
urlpatterns = [
    path('', views.MyListView.as_view(model=Users), name='list'),
    path('get_users/', views.getFollowers, name='get_followers'),
]

