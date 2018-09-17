# Create your models here.
# coding: utf-8
from django.db import models
from datetime import date

class T_TRG_PRM_MS(models.Model):
    trg_prm_cd          = models.IntegerField(primary_key=True)
    trg_prm_name        = models.CharField(max_length=64)
    find_tag            = models.CharField(max_length=64)
    class_string        = models.CharField(max_length=128)
    exclude_tags        = models.CharField(max_length=2048)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_SCALE_MS(models.Model):
    scale_cd            = models.IntegerField(primary_key=True)
    scale_name          = models.CharField(max_length=128)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_INDUSTRY_MS(models.Model):
    industry_cd         = models.IntegerField(primary_key=True)
    industry_name       = models.CharField(max_length=128)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_BLAND_MS(models.Model):
    bland_cd            = models.IntegerField(primary_key=True)
    bland_name          = models.CharField(max_length=128)
    market_prod_cls     = models.CharField(max_length=64)
    industry_cd         = models.ForeignKey(T_INDUSTRY_MS,on_delete=models.CASCADE)
    sub_industry_cd     = models.IntegerField()
    scale_cd            = models.ForeignKey(T_SCALE_MS,on_delete=models.CASCADE)
    fetch_flg           = models.BooleanField(default=True)
    access_url_string   = models.URLField(max_length=2083)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_STK_PRC_TR(models.Model):
    bland_cd            = models.ForeignKey(T_BLAND_MS,on_delete=models.CASCADE)
    market_prod_cls     = models.CharField(max_length=64)
    current_price       = models.IntegerField()
    day_before_ratio    = models.CharField(max_length=64)
    opening_price       = models.IntegerField()
    high_orice          = models.IntegerField()
    low_price           = models.IntegerField()
    sales_volume        = models.IntegerField()
    created_at          = models.DateTimeField(auto_now_add=True)
