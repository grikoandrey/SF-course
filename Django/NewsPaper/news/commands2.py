from news.models import *
from faker import Faker
import random

fake = Faker()

# Очищаем базу
User.objects.all().delete()
Category.objects.all().delete()
Author.objects.all().delete()
Post.objects.all().delete()
Comment.objects.all().delete()

# Создаем пользователей
user1 = User.objects.create_user('jamesW92', first_name='James', last_name='Whitaker')
user2 = User.objects.create_user('emilyH_01', first_name='Emily', last_name='Harper')
user3 = User.objects.create_user('oliverB_88', first_name='Oliver', last_name='Bennett')
user4 = User.objects.create_user('sophiaC24', first_name='Sophia', last_name='Carter')
user5 = User.objects.create_user('liamM07', first_name='Liam', last_name='Miller')
user6 = User.objects.create_user('avaT33', first_name='Ava', last_name='Taylor')

# Создаем авторов (первые 4 пользователя)
author1 = Author.objects.create(author_name=user1)
author2 = Author.objects.create(author_name=user2)
author3 = Author.objects.create(author_name=user3)
author4 = Author.objects.create(author_name=user4)

authors = [author1, author2, author3, author4]

# Создаем категории
cat1 = Category.objects.create(category_name='policy')
cat2 = Category.objects.create(category_name='sport')
cat3 = Category.objects.create(category_name='music')
cat4 = Category.objects.create(category_name='education')
categories = [cat1, cat2, cat3, cat4]

# Создаем 10 постов (новости и статьи поочередно)
posts = []
for i in range(40):
    author = random.choice(authors)
    post_type = 'AR' if i % 2 == 0 else 'NW'  # поочередно статья и новость
    post = Post.objects.create(
        post_author=author,
        post_type=post_type,
        post_title=fake.text(max_nb_chars=20),
        post_text=fake.text(max_nb_chars=1250)
    )
    # Рандомно добавляем 1-2 категории
    post.post_category.add(*random.sample(categories, random.randint(1, 2)))
    posts.append(post)

# Создаем 30-40 комментариев и привязываем к случайным постам
for _ in range(random.randint(55, 60)):
    post = random.choice(posts)
    user = random.choice([user1, user2, user3, user4, user5, user6])
    comment = Comment.objects.create(
        comment_text=fake.text(max_nb_chars=60),
        comment_post=post,
        comment_author=user
    )
    # Рандомно ставим лайк/дизлайк
    for _ in range(random.randint(0, 5)):
        comment.like()
    for _ in range(random.randint(0, 3)):
        comment.dislike()

# Рандомно ставим лайки/дизлайки для постов
for post in posts:
    for _ in range(random.randint(0, 10)):
        post.like()
    for _ in range(random.randint(0, 5)):
        post.dislike()
