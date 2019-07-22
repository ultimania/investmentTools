from django.urls import path, include
from . import views
 
app_name = 'accounts'
 
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_done/', views.SignUpDoneView.as_view(), name='signup_done'),
    path('signup_complete/<token>', views.SignUpCompleteView.as_view(), name='signup_complete'),
    path('delete/<int:pk>/', views.DeleteUserView.as_view(), name='delete'),
]
