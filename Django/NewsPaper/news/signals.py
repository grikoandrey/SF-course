from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from django.template.loader import render_to_string

from news.models import Post


@receiver(post_save, sender=Post)
def notify_managers(sender, instance, created, **kwargs):
    if created:
        subject = f'Created {instance.post_title} at {instance.post_created.strftime("%d.%m.%Y")}'
    else:
        subject = f'Changed {instance.post_title} at {instance.post_created.strftime("%d.%m.%Y")}'
    mail_managers(
        subject=subject,
        message=instance.post_text,
    )


@receiver(post_delete, sender=Post)
def notify_managers_on_delete(sender, instance, **kwargs):
    subject = f'{instance.post_title} was deleted'
    message = render_to_string("emails/manager_post_notification.txt", {
        'post': instance,
        'action': "удалён",
    })
    mail_managers(
        subject=subject,
        message=message,
    )


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    if instance.pk:  # если редактирование, пропускаем
        return
    posts_today = Post.objects.filter(
        post_author=instance.post_author,
        post_created__date=timezone.now().date()
    ).count()

    if posts_today >= 3:
        raise ValidationError("You can't create more than 3 posts per day.")
