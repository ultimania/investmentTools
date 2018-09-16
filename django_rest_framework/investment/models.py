from django.db import models

# Create your models here.
# coding: utf-8
from django.db import models
from datetime import date

class Investment(models.Model):
    bland_cd = models.CharField(primary_key=True, max_length=11)
    market_prod_cls = models.CharField(max_length=2048)
    current_price = models.CharField(max_length=11)
    day_before_ratio = models.CharField(max_length=2048)
    opening_price = models.CharField(max_length=11)
    high_price = models.CharField(max_length=11)
    low_price = models.CharField(max_length=11)
    sales_volume = models.CharField(max_length=11)
    create_timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publishing = models.BooleanField(default=True)
