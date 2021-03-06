# Create your models here.
# coding: utf-8
from django.db import models
from django.utils import timezone

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
    market_prod_cls     = models.CharField(max_length=256)
    current_price       = models.FloatField()
    day_before_ratio    = models.CharField(max_length=64)
    opening_price       = models.FloatField()
    high_orice          = models.FloatField()
    low_price           = models.FloatField()
    sales_volume        = models.IntegerField()
    created_at          = models.DateTimeField(auto_now_add=True)

class T_STATISTIC_MS(models.Model):
    statistic_cd        = models.IntegerField(primary_key=True)
    statistic_name      = models.CharField(max_length=1024)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_UNIT_MS(models.Model):
    unit_cd             = models.IntegerField(primary_key=True)
    unit_name           = models.CharField(max_length=1024)
    created_at          = models.DateTimeField(auto_now_add=True)


class T_CONDITIONS_MS(models.Model):
    conditions_cd       = models.IntegerField(primary_key=True)
    conditions_name     = models.CharField(max_length=1024)
    created_at          = models.DateTimeField(auto_now_add=True)


class T_EXT_CND_TR(models.Model):
    condition_no        = models.IntegerField(primary_key=True)
    condition_name      = models.CharField(max_length=1024)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_EXT_CND_CH_TR(models.Model):
    condition_ch_no     = models.IntegerField(primary_key=True)
    condition_no        = models.ForeignKey(T_EXT_CND_TR,on_delete=models.CASCADE)
    condition_type      = models.CharField(max_length=256)
    target0             = models.ForeignKey(T_TRG_PRM_MS,on_delete=models.CASCADE)
    target1             = models.ForeignKey(T_STATISTIC_MS,on_delete=models.CASCADE)
    threshold           = models.IntegerField()
    conditions          = models.ForeignKey(T_CONDITIONS_MS,on_delete=models.CASCADE)
    unit                = models.ForeignKey(T_UNIT_MS,on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)

class T_URL_MS(models.Model):
    url_cd              = models.IntegerField(primary_key=True)
    url_str             = models.CharField(max_length=128)
    tag_cd              = models.IntegerField()
    pages               = models.IntegerField()
    get_flg             = models.IntegerField()

