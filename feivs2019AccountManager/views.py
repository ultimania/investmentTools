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

# GET /twitter/arrange_follow リクエストを受けて呼び出される
def arrangeFollow(request):
    model = Users()
    model_manager = UsersManager()
    model_manager.arrangeFollow()
    return render(request, 'feivs2019AccountManager/blank.html')

# GET /twitter/myretweet リクエストを受けて呼び出される
def retweetMytweet(request):
    model = MyTweets()
    model_manager = MyTweetsManager()
    model_manager.retweetMytweet()
    return render(request, 'feivs2019AccountManager/blank.html')

# GET /twitter/get_users リクエストを受けて呼び出される
def getFollowers(request):
    get_mode = request.GET.get('get_mode')
    diff_mode = request.GET.get('diff_mode')
    get_flg = {'follower': True, 'friend': False}
    model_manager = UsersManager()

    if diff_mode == 'False':
        model_manager.getUsers(user_flg=get_flg[get_mode], diff_mode=False)
    else:
        model_manager.getUsers(user_flg=get_flg[get_mode])

    model_manager.getUsersStatics()
    return render(request, 'feivs2019AccountManager/blank.html')

# GET /twitter/refavorite リクエストを受けて呼び出される
def refavorite(request):
    model_manager = UsersManager()
    mode = request.GET.get('mode')

    model_manager.refavorite(mode=mode)
    return render(request, 'feivs2019AccountManager/blank.html')

# GET /twitter/favorite リクエストを受けて呼び出される
def favorite(request):
    model_manager = UsersManager()
    keyword = request.GET.get('keyword')
    # 特定のワードに変換
    if keyword == 'tag_studyprogram':
        keyword = '#プログラミング学習'
    model_manager.favorite(keyword=keyword)
    return render(request, 'feivs2019AccountManager/blank.html')
