from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib import messages

from news.models import Author
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'


@login_required
def toggle_author_status(request):
    user = request.user
    group_authors = Group.objects.get(name='Authors')

    # Если пользователь уже автор — снимаем статус
    if user.groups.filter(name='Authors').exists():
        group_authors.user_set.remove(user)

        # Удаляем объект Author, если он есть
        Author.objects.filter(author_name=user).delete()
        messages.success(request, "Статус автора удален. Теперь вы обычный пользователь.")
    else:
        # Если пользователь еще не автор — добавляем
        group_authors.user_set.add(user)
        Author.objects.get_or_create(author_name=user)
        messages.success(request, "Вы стали автором!")

    return redirect('/news/')
