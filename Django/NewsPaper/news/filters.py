import django_filters
from django import forms
from django_filters import FilterSet

from .models import Post, Category


class PostFilter(FilterSet):
    post_created = django_filters.DateFilter(
        field_name='post_created',
        lookup_expr='gt',
        label='Date later then',
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    post_category = django_filters.ModelMultipleChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Category',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-checkboxes'}),
    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'post_author__author_name__username': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['post_title__icontains'].label = 'Title contain'
        self.form.fields['post_author__author_name__username__icontains'].label = 'Author'
