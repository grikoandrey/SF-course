from django.urls import path
from .views import PostList, PostDetail, SearchPostList, PostCreate, PostEdit, PostDelete, Subscription

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('search/', SearchPostList.as_view(), name='search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('subscription/', Subscription.as_view(), name='subscription'),
]
