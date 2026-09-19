from app.workers.celery_app import celery_app


@celery_app.task
def health_check_task() -> str:
    return "ok"