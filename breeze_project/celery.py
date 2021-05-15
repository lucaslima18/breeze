from __future__ import absolute_import
from utils.tasks import playlist_objects_info
from django.conf import settings  # noqa

import os

from celery import Celery

'''
    here i define the celery configuration for call one function for
    return all playlist objects in database
'''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breeze_project.settings')

app = Celery('breeze_project')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    "listing-playlists": {
        "task": playlist_objects_info(),
        "schedule": 60.0
    }
}
