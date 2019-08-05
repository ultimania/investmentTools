from django.shortcuts import render
from django.views import generic
from .models import LearnManager, UserAnalistics

class MyListView(generic.ListView):
    model = UserAnalistics
    context_object_name = 'users'
    paginate_by = 30
    template_name = 'learntweet/analistics_list.html'

    def get_queryset(self):
        queryset = UserAnalistics.objects.all().order_by('-similarity')
        return queryset

# Create your views here.
def learningView(request):
    MIN_SIMILARITY = 1.0
    RELATE_STORE_NUM = 20

    user_mode = request.GET.get('user')
    relearn_mode = request.GET.get('relearn')
    model_manager = LearnManager(user_mode, relearn_mode)
    import pdb;pdb.set_trace()
    # LDAを作成
    model_manager.createLDA()
    # 他人のタイムラインを取得・分析
    model_manager.analysTweets(MIN_SIMILARITY, RELATE_STORE_NUM)
    return render(request, 'learntweet/blank.html')