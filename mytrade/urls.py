from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('bland/', views.bland, name='bland'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]

