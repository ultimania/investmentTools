from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('mytrade/', include(('mytrade.urls', 'mytrade'),)),
    path('admin/', admin.site.urls),
]
