from django_apscheduler.models import DjangoJobExecution


def delete_old_job_executions(max_age=604_800):
    """Удаляет старые записи о выполнениях задач (по умолчанию старше 7 дней)."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
