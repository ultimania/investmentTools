# coding: utf-8
from rest_framework import serializers
from .models import Investment


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            'bland_cd', 
            'market_prod_cls', 
            'current_price', 
            'day_before_ratio',
            'opening_price',
            'high_price',
            'low_price',
            'sales_volume',
            'create_timestamp',
        )

