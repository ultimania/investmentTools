from django.views import generic
from django.shortcuts import get_object_or_404, render
from .models import Users, UsersManager, MyTweets, MyTweetsManager
from django.db import utils
from django.db.models import Count
from rest_framework import viewsets

# Create your views here.
class MyListView(generic.ListView):
    model = Users
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'feivs2019AccountManager/follower_list.html'

    def get_queryset(self):
        queryset = Users.objects.filter(favourites_cnt_for_me__gt=0).order_by('-favourites_cnt_for_me')
        return queryset

# GET /twitter/myretweet リクエストを受けて呼び出される
def retweetMytweet(request):
    model = MyTweets()
    model_manager = MyTweetsManager()
    model_manager.retweetMytweet()
    return render(request, 'feivs2019AccountManager/follower_list.html')

# GET /twitter/get_users リクエストを受けて呼び出される
def getFollowers(request):
    get_mode = request.GET.get('get_mode')
    get_flg = {'follower': True, 'friend': False}
    update_column = {'follower': 'follower_flg', 'friend': 'follow_flg'}
    udpate_data = {update_column[get_mode]: True}

    model = Users()
    model_manager = UsersManager()
    user_model_data = []
    cursor = -1
    
    while cursor != 0:
        cursor = model_manager.getUsers(cursor, user_model_data, get_flg=get_flg[get_mode])
        for data in user_model_data :
            try:
                if Users.objects.filter(user_id=data['user_id']).update(**data) == 0:
                    Users.objects.filter(user_id=data['user_id']).create(**data)
            except :
                import traceback; traceback.print_exc()
                pass
    user_model_data = {}
    model_manager.getUsersStatics(user_model_data)
    for user_id, data in user_model_data.items():
        Users.objects.filter(user_id=user_id).update(**data)
    return render(request, 'feivs2019AccountManager/follower_list.html')
