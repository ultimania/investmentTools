# coding: utf-8
from rest_framework import routers

from .views import TargetParamViewSet
from .views import ScaleViewSet
from .views import IndustryViewSet
from .views import BlandViewSet
from .views import StockPriceViewSet
from .views import StatisticViewSet
from .views import UnitViewSet
from .views import ConditionsViewSet
from .views import ExtractionConditionViewSet
from .views import ExtractionConditionChildViewSet

router = routers.DefaultRouter()
router.register(r'targetparam', TargetParamViewSet)
router.register(r'scale', ScaleViewSet)
router.register(r'industry', IndustryViewSet)
router.register(r'bland', BlandViewSet)
router.register(r'stockprice', StockPriceViewSet)
router.register(r'statistic', StatisticViewSet)
router.register(r'unit', UnitViewSet)
router.register(r'conditions', ConditionsViewSet)
router.register(r'extractioncondition', ExtractionConditionViewSet)
router.register(r'extractionconditionchild', ExtractionConditionChildViewSet)

