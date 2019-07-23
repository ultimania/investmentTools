from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mytrade/', include(('mytrade.urls', 'mytrade'),)),
    path('accounts/', include(('accounts.urls', 'accounts'),)),
    path('accounts/', include(('django.contrib.auth.urls'),)),
    path('twitter/', include(('feivs2019AccountManager.urls', 'twitter'),)),
]
