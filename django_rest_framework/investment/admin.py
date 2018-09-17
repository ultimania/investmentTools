from django.contrib import admin

# Register your models here.
# coding: utf-8
from django.contrib import admin
from .models import T_TRG_PRM_MS
from .models import T_SCALE_MS
from .models import T_INDUSTRY_MS
from .models import T_BLAND_MS
from .models import T_STK_PRC_TR

@admin.register(T_TRG_PRM_MS)
class T_TRG_PRM_MS(admin.ModelAdmin):
    pass

@admin.register(T_SCALE_MS)
class T_SCALE_MS(admin.ModelAdmin):
    pass

@admin.register(T_INDUSTRY_MS)
class T_INDUSTRY_MS(admin.ModelAdmin):
    pass

@admin.register(T_BLAND_MS)
class T_BLAND_MS(admin.ModelAdmin):
    pass

@admin.register(T_STK_PRC_TR)
class T_STK_PRC_TR(admin.ModelAdmin):
    pass

