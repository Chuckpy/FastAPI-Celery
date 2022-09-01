import os
from celery import Celery

user = os.getenv('POSTGRES_USER', '')
password = os.getenv('POSTGRES_PASSWORD', '')
db = os.getenv('POSTGRES_DB', '')

celery_app = Celery("worker", broker="amqp://guest:guest@rabbitmq:5672//", backend=f"postgresql://{user}:{password}@db/{db}")
celery_app.conf.task_routes = {"src.celery.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)

