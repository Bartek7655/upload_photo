import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "upload_photo_backend.settings")
app = Celery("upload_photo_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
