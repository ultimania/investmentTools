from feivs2019AccountManager.models import *
from django.shortcuts import render
from django.views import generic
from .models import LearnManager, UserAnalistics
import pandas as pd


class MyListView(generic.ListView):
    model = UserAnalistics
    context_object_name = 'users'
    paginate_by = 30
    template_name = 'learntweet/analistics_list.html'

    def get_queryset(self):
        queryset = UserAnalistics.objects.all().order_by('-similarity')
        return queryset

class DisplayView(generic.ListView):
    # model = Users
    context_object_name = 'context'
    template_name = 'learntweet/analistics_detail.html'

    def get_queryset(self):
        queryset = Users.objects.filter(screen_name=self.kwargs.get('pk')).get()
        return queryset

    def get_context_data(self, **kwargs):
        model_manager = LearnManager()
        # import pdb;pdb.set_trace()        
        kwargs['df'] = model_manager.displayAnalistics(id=self.kwargs.get('pk'),MIN_SIMILARITY=5 ).values.tolist()
        return super().get_context_data(**kwargs)


def learningView(request):
    #import pdb;pdb.set_trace()
    user_mode = request.GET.get('user')
    relearn_mode = request.GET.get('relearn')
    model_manager = LearnManager(user_mode, relearn_mode)

    # 各種パラメータを設定
    USER_COUNT = 700
    TIMELINE_COUNT = 50

    # LDA分類機を作成
    model_manager.createLDA()

    # 分析対象のトピックスを取得して分析
    # topics = model_manager.getTopicsFromTweets(USER_COUNT, TIMELINE_COUNT)
    # import pdb;pdb.set_trace()
    topics = pd.DataFrame(list(UserAnalistics.objects.all().values('screen_name', 'name', 'text')))
    topics.rename(columns={"screen_name": "id"}, inplace=True)
    model_manager.calcLdaVector(topics)
    model_manager.createModelFromTopics(topics)

    return render(request, 'learntweet/blank.html')
