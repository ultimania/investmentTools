from django.views import generic
from django.shortcuts import render
from .models import Users, UsersManager
from django.db import utils

# Create your views here.
class MyListView(generic.ListView):
    paginate_by = 10
    template_name = 'feivs2019AccountManager/follower_list.html'

def getFollowers(request):
    get_mode = request.GET.get('get_mode')
    get_flg = {'follower': True, 'friend': False}

    model = Users()
    model_manager = UsersManager()
    user_model_data = []
    cursor = -1
    
    while cursor != 0:
        cursor = model_manager.getUsers(cursor, user_model_data,get_flg=get_flg[get_mode])
        for data in user_model_data :
            try:
                Users.objects.update_or_create(**data)
            except utils.InternalError as e:
                print(e)
                pass
    #model.getFollowersStatics()
    return render(request, 'feivs2019AccountManager/follower_list.html')
