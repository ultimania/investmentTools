from django.shortcuts import render

# Create your views here.
# coding: utf-8
from rest_framework import viewsets
from .models import Investment
from .serializer import InvestmentSerializer


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

