# coding: utf-8
from rest_framework import serializers
from .models import T_TRG_PRM_MS
from .models import T_SCALE_MS
from .models import T_INDUSTRY_MS
from .models import T_BLAND_MS
from .models import T_STK_PRC_TR
from .models import T_EXT_CND_TR
from .models import T_EXT_CND_CH_TR
from .models import T_STATISTIC_MS
from .models import T_UNIT_MS
from .models import T_CONDITIONS_MS


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
    industry_cd = IndustrySerializer()
    scale_cd = ScaleSerializer()
    class Meta:
        model = T_BLAND_MS
        fields = '__all__' 

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_STK_PRC_TR
        fields = '__all__' 

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_STATISTIC_MS
        fields = '__all__' 

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_UNIT_MS
        fields = '__all__' 

class ConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_CONDITIONS_MS
        fields = '__all__' 

class ExtractionConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = T_EXT_CND_TR
        fields = '__all__' 

class ExtractionConditionChildSerializer(serializers.ModelSerializer):
    target0 = TargetParamSerializer
    target1 = StatisticSerializer
    unit    = UnitSerializer
    class Meta:
        model = T_EXT_CND_CH_TR
        fields = '__all__' 


