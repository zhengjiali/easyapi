from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easyapi.seettings")

app = Celery('easyapi')
app.config_from_object('django.conf:settings','CELERY')
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))