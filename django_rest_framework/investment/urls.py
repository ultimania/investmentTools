# coding: utf-8
from rest_framework import routers

from .views import TargetParamViewSet
from .views import ScaleViewSet
from .views import IndustryViewSet
from .views import BlandViewSet
from .views import StockPriceViewSet

router = routers.DefaultRouter()
router.register(r'targetparam', TargetParamViewSet)
router.register(r'scale', ScaleViewSet)
router.register(r'industry', IndustryViewSet)
router.register(r'bland', BlandViewSet)
router.register(r'stockprice', StockPriceViewSet)
