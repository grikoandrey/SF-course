from django.urls import path
from .views import ArticleCreate

urlpatterns = [
    path('create/', ArticleCreate.as_view(), name='article_create'),
]
