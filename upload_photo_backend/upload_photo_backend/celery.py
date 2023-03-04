import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "upload_photo_backend.settings")
app = Celery("upload_photo_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-binary-links': {
        'task': 'main.tasks.delete_expired_binary_links',
        'schedule': 300,
    }
}
