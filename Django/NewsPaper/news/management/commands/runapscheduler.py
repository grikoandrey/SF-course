import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from news.jobs import delete_old_job
from news.jobs.weekly_notifications import send_weekly_notifications

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # 1. Еженедельная рассылка (например, каждое воскресенье в 9 утра)
        scheduler.add_job(
            send_weekly_notifications,
            trigger=CronTrigger(day_of_week="mon", hour="6", minute="0"),
            id="weekly_notifications",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_notifications'.")

        # 2. Очистка старых job executions
        scheduler.add_job(
            delete_old_job,
            trigger=CronTrigger(day_of_week="mon", hour="0", minute="0"),
            id="delete_old_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
