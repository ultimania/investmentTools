from django.shortcuts import render
from django.http.response import HttpResponse
import sys

from .models import T_BLAND_MS
from .models import T_STK_PRC_TR

# Render Index Page
def index(request):
    return render(request, 'index.haml')

# Render Bland Page
def bland(request):
    req_bland_cd = request.GET.get('bland_cd')

    #銘柄情報取得
    bland_info = T_BLAND_MS.objects.filter(bland_cd=req_bland_cd).values(
        'bland_cd',
        'bland_name',
        'market_prod_cls',
    )
    stock_info = T_STK_PRC_TR.objects.filter(bland_cd=req_bland_cd).values()

    params = {
        'bland_info'        : bland_info[0],
        'stock_info'        : stock_info[0],
    }

    return render(request, 'bland.haml', params)
