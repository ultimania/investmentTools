from django.views import generic
from django.shortcuts import render

from .models import user

# Create your views here.
class MyListView(generic.ListView):
    model = user()
    '''
    model.getFollowers()
    model.getFollowersStatics()
    '''
    paginate_by = 10