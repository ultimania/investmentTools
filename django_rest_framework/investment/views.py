from django.shortcuts import render

# Create your views here.
# coding: utf-8
from rest_framework import viewsets
from .models import T_TRG_PRM_MS
from .models import T_SCALE_MS
from .models import T_INDUSTRY_MS
from .models import T_BLAND_MS
from .models import T_STK_PRC_TR

from .serializer import TargetParamSerializer
from .serializer import ScaleSerializer
from .serializer import IndustrySerializer
from .serializer import BlandSerializer
from .serializer import StockPriceSerializer

class TargetParamViewSet(viewsets.ModelViewSet):
    queryset = T_TRG_PRM_MS.objects.all()
    serializer_class = TargetParamSerializer

class ScaleViewSet(viewsets.ModelViewSet):
    queryset = T_SCALE_MS.objects.all()
    serializer_class = ScaleSerializer

class IndustryViewSet(viewsets.ModelViewSet):
    queryset = T_INDUSTRY_MS.objects.all()
    serializer_class = IndustrySerializer

class BlandViewSet(viewsets.ModelViewSet):
    queryset = T_BLAND_MS.objects.all()
    serializer_class = BlandSerializer

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = T_STK_PRC_TR.objects.all()
    serializer_class = StockPriceSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = T_STK_PRC_TR.objects.all()

        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(bland_cd=query).distinct()
        return queryset_list

