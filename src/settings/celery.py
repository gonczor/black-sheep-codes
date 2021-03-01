import os

import environ
from celery import Celery
from celery.signals import task_failure

env = environ.Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app = Celery("blacksheeplearns")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


if bool(env.bool("ROLLBAR_ENABLED", False)):
    import rollbar
    from django.conf import settings

    rollbar.init(**settings.ROLLBAR)

    def celery_base_data_hook(request, data):
        data["framework"] = "celery"

    rollbar.BASE_DATA_HOOK = celery_base_data_hook

    @task_failure.connect
    def handle_task_failure(**kw):
        rollbar.report_exc_info(extra_data=kw)
