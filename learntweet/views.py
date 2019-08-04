from django.shortcuts import render

# Create your views here.
def learningView(request):
    import pdb;pdb.set_trace()
    model_manager = LearnManager()
    # LDAを作成
    model_manager.createLDA()
    # 他人のタイムラインを取得・分析
    mode = 'follower'
    MIN_SIMILARITY = 0.6  # 類似度のしきい値
    RELATE_STORE_NUM = 20  # 似ている店の抽出数
    model_manager.analysTweets(mode, MIN_SIMILARITY, RELATE_STORE_NUM)
    return render(request, 'learntweet/blank.html')