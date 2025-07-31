from django.contrib.auth.models import User
from django.db import models
# from django.db.models import Sum
# from django.utils import timezone


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        # 1. Суммарный рейтинг всех постов автора * 3
        post_rating = (Post.objects.filter(post_author=self)
                       .aggregate(total=models.Sum('post_rating')).get('total', 0))

        # 2. Суммарный рейтинг всех комментариев, оставленных автором
        comment_rating = (Comment.objects.filter(comment_author=self.author_name)
                          .aggregate(total=models.Sum('comment_rating'))['total'] or 0)

        # 3. Суммарный рейтинг всех комментариев ко всем постам автора
        comments_to_posts_rating = (Comment.objects.filter(comment_post__post_author=self)
                                    .aggregate(total=models.Sum('comment_rating'))['total'] or 0)

        # Итоговый рейтинг
        self.author_rating = post_rating * 3 + comment_rating + comments_to_posts_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)


class Post(models.Model):
    ARTICLE, NEWS = 'AR', 'NW'

    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default='AR')
    post_created = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory', blank=True)
    post_title = models.CharField(max_length=100)
    post_text = models.TextField()
    post_rating = models.FloatField(default=0.0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.post_text[:124]}...' if len(self.post_text) > 124 else self.post_text


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
