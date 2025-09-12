import logging
from smtplib import SMTPException

from django.core.mail import send_mail
from django.conf import settings
from django.http import BadHeaderError
from django.utils import timezone
from datetime import timedelta

from news.models import Post, Category

logger = logging.getLogger(__name__)


def send_weekly_notifications():
    """
    Отправляет пользователям подборку постов по всем их категориям за неделю.
    Каждый пользователь получает одно письмо.
    """

    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(post_created__gte=last_week)

    if not posts.exists():
        logger.info("Новых постов за неделю нет.")
        return

    # Собираем словарь: user -> {category: [posts]}
    user_posts = {}

    for category in Category.objects.all():
        category_posts = posts.filter(post_category=category)
        if not category_posts.exists():
            continue

        for user in category.subscribers.all():
            if user not in user_posts:
                user_posts[user] = {}
            user_posts[user][category] = category_posts

    # Рассылаем письма
    for user, categories_dict in user_posts.items():
        subject = "Еженедельная подборка новых публикаций"
        message_lines = [f"Здравствуйте, {user.username}! Вот новые публикации за неделю:\n"]

        for category, category_posts in categories_dict.items():
            message_lines.append(f"\nКатегория: {category.category_name}")
            for p in category_posts:
                message_lines.append(f" - {p.post_title} → читать полностью: {settings.SITE_URL}{p.get_absolute_url()}")

        message = "\n".join(message_lines)

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            logger.info(f"Отправлено письмо пользователю {user.username}")
        except (SMTPException, BadHeaderError) as e:
            logger.exception(f"Ошибка отправки письма пользователю {user.username}: {e}")
