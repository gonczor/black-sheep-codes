import os

import environ
import kombu
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


with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='myexchange',
        type='fanout',
        durable=True,
        channel=conn,
    )
    exchange.declare()
    queue = kombu.Queue(
        name='myqueue',
        exchange=exchange,
        routing_key='mykey',
        channel=conn,
        # message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()
    queue = kombu.Queue(
        name='myotherqueue',
        exchange=exchange,
        routing_key='mykey',
        channel=conn,
        # message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()
