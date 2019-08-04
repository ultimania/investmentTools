from django.urls import path, include
from . import views
from .models import Users
urlpatterns = [
    path('', views.MyListView.as_view(), name='list'),
    path('learning/', views.learningView(), name='learning'),
]
