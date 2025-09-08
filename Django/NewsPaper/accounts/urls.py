from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import BaseRegisterView, toggle_author_status

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='accounts/signup.html'), name='signup'),
    path('author/', toggle_author_status, name='toggle_author_status'),
]
