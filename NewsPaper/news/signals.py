# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Post
#
#
# @receiver(post_save, sender=Post)
# def product_created(instance, **kwargs):
#     print('New post is created', instance)
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__postCategory=instance.postCategory
    ).values_list('email', flat=True)

    subject = f'New post about {instance.postCategory} is available'

    text_content = (
        f'Post: {instance.title}\n'
        f'Type: {instance.categoryType}\n'
        f'Category: {instance.postCategory}\n\n'
        f'Link to the post: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Post: {instance.title}<br>'
        f'Type: {instance.categoryType}<br>'
        f'Category: {instance.postCategory}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Link to the post</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()