from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('twitter/', include(('feivs2019AccountManager.urls', 'twitter'),)),
    path('learn/', include(('learntweet.urls', 'learn'),)),
]
