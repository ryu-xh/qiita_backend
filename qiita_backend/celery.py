import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qiita_backend.settings')
app = Celery('qiita_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

