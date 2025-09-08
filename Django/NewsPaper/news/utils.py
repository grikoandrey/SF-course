from django.core.mail import EmailMultiAlternatives, mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string


def send_notifications(post, user):
    categories = post.post_category.all()
    subscribers = set()
    for category in categories:
        subscribers.update(category.subscribers.all())

    if not subscribers:
        return

    context = {
        'post': post,
        'username': user.username,
        'categories': categories,
    }

    html_content = render_to_string('post_created.html', context)
    msg = EmailMultiAlternatives(
        subject=f'Новый пост в категориях: {", ".join([c.category_name for c in categories])}',
        body=post.post_text,
        from_email='griko.andrey@yandex.ru',
        to=['griko.and@gmail.com', 'griko_aa@mail.ru'],
        # to=[user.email for user in subscribers if user.email],
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем
