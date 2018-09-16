from django.contrib import admin

# Register your models here.
# coding: utf-8
from django.contrib import admin
from .models import Investment


@admin.register(Investment)
class Investment(admin.ModelAdmin):
    pass
