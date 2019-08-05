from django.shortcuts import render
from django.views import generic
from .models import LearnManager, UserAnalistics

class MyListView(generic.ListView):
    model = UserAnalistics
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'learntweet/analistics_list.html'

# Create your views here.
def learningView(request):
    model_manager = LearnManager()
    # LDAを作成
    model_manager.createLDA()
    user = request.GET.get('user')
    # 他人のタイムラインを取得・分析
    if user == 'follower':
        mode = True
    else:
        mode = False

    mode = True #debug
    MIN_SIMILARITY = 1.0
    RELATE_STORE_NUM = 20
    model_manager.analysTweets(mode, MIN_SIMILARITY, RELATE_STORE_NUM)
    return render(request, 'learntweet/blank.html')