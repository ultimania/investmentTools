from django.shortcuts import render
from django.http.response import HttpResponse
import sys, io
from . import displayer
from . import analyzer

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Render Index Page
def index(request):
    return render(request, 'index.haml')

# Render Bland Page
def bland(request):
    # クエリパラメータの取得
    req_bland_cd = request.GET.get('bland_cd')
    req_sample_mode = request.GET.get('sample_mode')

    # モデルデータの取得とチャート作成
    model_data = displayer.getModelData(req_bland_cd)
    displayer.generateChart('T_STK_PRC_TR', model_data, req_sample_mode)
    params = displayer.getParams('T_STK_PRC_TR', model_data)

    # 株価データの学習と予測結果の取得
    pred_result = analyzer.learnSvm(req_bland_cd)
    params.update({'pred_result' : pred_result})

    return render(request, 'bland.html', params)

