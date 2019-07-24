from django.urls import path, include
from . import views
from .models import Users
urlpatterns = [
    path('', views.MyListView.as_view(model=Users), name='list'),
    path('get_gollowers/', views.getFollowers, name='get_gollowers'),
]

