from django.contrib import admin
from django.urls import path, include

from news.views import ContactsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('articles/', include('news.urls_articles')),
    path('sign/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
