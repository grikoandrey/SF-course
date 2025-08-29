from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post
from django.utils import timezone


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
        post_type = form.save(commit=False)
        post_type.post_type = 'NW'
        messages.success(self.request, "Новость успешно создана!")
        return super().form_valid(form)

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
        messages.success(self.request, "Статья успешно создана!")
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, "Для создания статьи стань автором!")
        return redirect('posts')


class ContactsView(TemplateView):
    template_name = 'flatpages/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return ctx
