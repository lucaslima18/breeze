from celery import celery_task


@celery_task()
def add():
    print("Hello world")