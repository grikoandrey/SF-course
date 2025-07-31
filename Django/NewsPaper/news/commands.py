# from django.contrib.auth.models import User
from news.models import *
from faker import Faker

fake = Faker()

User.objects.all().delete()
Category.objects.all().delete()

user1 = User.objects.create_user('user1', first_name='Name1')
user2 = User.objects.create_user('user2', first_name='Name2')

author1 = Author.objects.create(author_name=user1)
author2 = Author.objects.create(author_name=user2)

cat1 = Category.objects.create(category_name='policy')
cat2 = Category.objects.create(category_name='sport')
cat3 = Category.objects.create(category_name='music')
cat4 = Category.objects.create(category_name='education')
print(Category.objects.all().values('category_name'))

article1 = Post.objects.create(post_author=author1, post_title=fake.text(max_nb_chars=20),
                               post_text=fake.text(max_nb_chars=199))
article2 = Post.objects.create(post_author=author2, post_title=fake.text(max_nb_chars=20),
                               post_text=fake.text(max_nb_chars=250))
news1 = Post.objects.create(post_author=author1, post_type='NW', post_title=fake.text(max_nb_chars=17),
                            post_text=fake.text(max_nb_chars=180))

article2.post_category.add(cat1)
article1.post_category.add(cat2, cat3)
news1.post_category.add(cat3, cat4)

comment1 = Comment.objects.create(comment_text=fake.text(max_nb_chars=60), comment_post=article1, comment_author=user1)
comment2 = Comment.objects.create(comment_text=fake.text(max_nb_chars=45), comment_post=article2, comment_author=user2)
comment3 = Comment.objects.create(comment_text=fake.text(max_nb_chars=64), comment_post=article1, comment_author=user2)
comment4 = Comment.objects.create(comment_text=fake.text(max_nb_chars=57), comment_post=news1, comment_author=user1)

article1.like()
article1.like()
article2.dislike()
news1.like()
news1.like()
news1.dislike()
comment1.like()
comment3.like()
comment3.like()
comment2.dislike()
comment4.dislike()
comment4.dislike()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.all().order_by('-author_rating').first()
print(f"Лучший пользователь: {best_author.author_name.username} с рейтингом: {best_author.author_rating}")

best_post = Post.objects.all().order_by('-post_rating').first()
print(
    f"Лучшая статья: {best_post.post_title}\n"
    f"текст: {best_post.preview()}\n"
    f"автор: {best_post.post_author.author_name.username}, "
    f"рейтинг: {best_post.post_rating}, "
    f""f"дата создания: {best_post.post_created.strftime('%d.%m.%Y %H:%M')}\n"
)

comments_to_best_post = Comment.objects.filter(comment_post=best_post)
print(f"Комментарии к статье:")
for comment in comments_to_best_post:
    print(
        f"комментарий: {comment.comment_text}\n"
        f"автор: {comment.comment_author.username}, "
        f"рейтинг: {comment.comment_rating}, "
        f"дата: {comment.comment_created.strftime('%d.%m.%Y %H:%M')}\n"
    )
