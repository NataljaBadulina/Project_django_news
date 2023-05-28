import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
#
# logger = logging.getLogger(__name__)
#
#
# def my_job():
#     # Your job processing logic here...
#     pass
#
#
# # The `close_old_connections` decorator ensures that database connections,
# # that have become unusable or are obsolete, are closed before and after your
# # job has run. You should use it to wrap any jobs that you schedule that access
# # the Django database in any way.
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     """
#     This job deletes APScheduler job execution entries older than `max_age`
#     from the database.
#     It helps to prevent the database from filling up with old historical
#     records that are no longer useful.
#
#     :param max_age: The maximum length of time to retain historical
#                     job execution records. Defaults to 7 days.
#     """
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             my_job,
#             trigger=CronTrigger(second="*/10"),  # Every 10 seconds
#             id="my_job",  # The `id` assigned to each job MUST be unique
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added weekly job: 'delete_old_job_executions'.")
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta, timezone
from news.models import Post, Subscription

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
logger = logging.getLogger(__name__)

# def my_job():
#     post_list = Post.objects.order_by('dateCreation')[:5]
#     text = '\n'.join(['{} - {}'.format(p.title, p.dateCreation) for p in post_list])
#     send_mail("The latest news", text)


def my_job():
    last_week = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers_emails = []
    posts_sent = None
    for cat in categories:
        subscribers = Subscription.objects.filter(category=cat)
        subscribers_emails += [s.user.email for s in subscribers]
        posts_sent=posts.filter(categories__name=cat)

    html_content = render_to_string('weekly_update.html',
                           {
                               'link': f'{settings.SITE_URL}/news/',
                               'posts': posts_sent,
                           }
                                    )
    msg = EmailMultiAlternatives(
                           subject='Weekly news since last week',
                           body='',
                           from_email=settings.DEFAULT_FROM_EMAIL,
                           to=subscribers_emails
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(minute="20", hour="18", day_of_week="fri"),
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="20"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

