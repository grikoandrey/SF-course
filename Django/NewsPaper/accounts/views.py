from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


@login_required
def to_be_author(request):
    user = request.user
    group_authors = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        group_authors.user_set.add(user)
    return redirect('/news/')
