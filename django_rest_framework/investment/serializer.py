# coding: utf-8
from rest_framework import serializers
from .models import T_TRG_PRM_MS
from .models import T_SCALE_MS
from .models import T_INDUSTRY_MS
from .models import T_BLAND_MS
from .models import T_STK_PRC_TR


class TargetParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_TRG_PRM_MS
        fields = '__all__' 

class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_SCALE_MS
        fields = '__all__' 

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = T_INDUSTRY_MS
        fields = '__all__' 

class BlandSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_BLAND_MS
        fields = '__all__' 

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_STK_PRC_TR
        fields = '__all__' 

