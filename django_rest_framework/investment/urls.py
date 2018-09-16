# coding: utf-8
from rest_framework import routers
from .views import InvestmentViewSet

router = routers.DefaultRouter()
router.register(r'investments', InvestmentViewSet)

