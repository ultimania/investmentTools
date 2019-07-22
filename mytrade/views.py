from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth.decorators import login_required

import sys
import io
from . import displayer
from . import analyzer

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# PageNation
def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return {'page_obj' : page_obj, 'paginator' : paginator}

# Render Login Page
def login(request):
    return render(request, 'login.html')

# Render Index Page
def index(request):
    return render(request, 'index.html')

# Render Bland Page
@login_required
def bland(request):
    # クエリパラメータの取得
    req_bland_cd = '' if request.GET.get('bland_cd') is None else request.GET.get('bland_cd')
    req_sample_mode = request.GET.get('sample_mode')

    # パラメータ判定
    if req_bland_cd == '':
        # モデルデータの取得
        render_file = 'bland_home.html'
        model_data = displayer.getModelData()
        params = paginate_query(request, model_data['T_BLAND_MS'], settings.PAGE_PER_ITEM)
    else:
        # モデルデータの取得とチャート作成
        render_file = 'bland.html'
        model_data = displayer.getModelData(req_bland_cd)
        displayer.generateChart('T_STK_PRC_TR', model_data, req_sample_mode)
        params = displayer.getParams('T_STK_PRC_TR', model_data)

        # 株価データの学習と予測結果の取得
        pred_result = analyzer.learnSvm(req_bland_cd)
        params.update({'pred_result': pred_result})

    # import pdb;pdb.set_trace()
    return render(request, render_file, params)
