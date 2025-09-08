from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category
from django.utils import timezone

from .utils import send_notifications


class PostList(ListView):
    model = Post
    ordering = '-post_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        context['total_posts'] = Post.objects.count()
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchPostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-post_created'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 2

    filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        post.post_author = self.request.user.author

        try:
            post.save()  # вызов pre_save сигнала
        except ValidationError as e:
            messages.error(self.request, e.message)
            return redirect('posts')  # или render на ту же форму

        response = super().form_valid(form)
        messages.success(self.request, "Новость успешно создана!")
        send_notifications(self.object, self.request.user)  # <-- отправляем письма подписчикам
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context

    def handle_no_permission(self):
        messages.error(self.request, "Для создания новости стань автором!")
        return redirect('posts')


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context

    def handle_no_permission(self):
        messages.error(self.request, "Для изменения поста стань автором!")
        return redirect('posts')


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

    permission_required = 'news.delete_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context

    def handle_no_permission(self):
        messages.error(self.request, "Для удаления поста стань автором!")
        return redirect('posts')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    permission_required = 'news.add_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context

    def form_valid(self, form):
        post_type = form.save(commit=False)
        post_type.type = 'AR'
        response = super().form_valid(form)
        messages.success(self.request, "Статья успешно создана!")
        send_notifications(self.object, self.request.user)  # тот же вызов
        return response

    def handle_no_permission(self):
        messages.error(self.request, "Для создания статьи стань автором!")
        return redirect('posts')


class ContactsView(TemplateView):
    template_name = 'flatpages/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return ctx


class Subscription(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'subscription.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_subscriptions'] = self.request.user.category_subscriptions.all()
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        """Обрабатываем нажатие кнопки подписки/отписки"""
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, pk=category_id)

        if request.user in category.subscribers.all():
            category.subscribers.remove(request.user)
            messages.info(request, f'Вы отписались от категории «{category.category_name}».')
        else:
            category.subscribers.add(request.user)
            messages.success(request, f'Вы подписались на категорию «{category.category_name}».')
        # остаёмся на той же странице
        return redirect('subscription')
