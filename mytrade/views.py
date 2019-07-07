from django.shortcuts import render
from django.http.response import HttpResponse

# Render Index Page
def index(request):
    return render(request, 'index.haml')

# Render Bland Page
def bland(request):
    return render(request, 'bland.html')
