# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Post
#
#
# @receiver(post_save, sender=Post)
# def product_created(instance, **kwargs):
#     print('New post is created', instance)
# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.conf import settings #
# from .models import PostCategory
# from django.template.loader import render_to_string #
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#     # emails = User.objects.filter(
#     #     subscriptions__postCategory=instance.postCategory
#     # ).values_list('email', flat=True)
#
#     emails = User.objects.filter(subscriptions__category=instance.postCategory).values_list('email', flat=True)
#
#     subject = f'New post about {instance.postCategory} is available'
#
#     text_content = (
#         f'Post: {instance.title}\n'
#         f'Type: {instance.categoryType}\n'
#         f'Category: {instance.postCategory}\n\n'
#         f'Link to the post: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = render_to_string(
#         f'Post: {instance.title}<br>'
#         f'Type: {instance.categoryType}<br>'
#         f'Category: {instance.postCategory}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Link to the post</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()

from django.contrib.auth.models import User

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory


def send_notifications(pk, title, subscribers):
    subject = f'New post about {PostCategory} is available'
    text_content = (
        f'Post: {title}\n'
        f'Link to the post: {settings.SITE_URL}/news/{pk}'
    )
    html_content = render_to_string(
        f'Post: {title}<br>'
        f'Category: {PostCategory}<br><br>'
        f'<a href="{settings.SITE_URL}/news/{pk}">'
        f'Link to the post</a>'
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.pk, instance.title, subscribers_emails)

