from django.contrib import admin
from .models import Author, Category, Post, Comment

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('category_name',)
    filter_horizontal = ('subscribers',)
