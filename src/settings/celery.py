import os

import environ
import kombu

from celery import Celery, bootsteps
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
        name="myexchange",
        type="direct",
        durable=True,
        channel=conn,
    )
    exchange.declare()
    queue1 = kombu.Queue(
        name="myqueue",
        exchange=exchange,
        routing_key="mykey",
        channel=conn,
        # message_ttl=600,
        # queue_arguments={
        #     "x-queue-type": "classic"
        # },
        durable=True
    )
    queue1.declare()
    queue2 = kombu.Queue(
        name="myotherqueue",
        exchange=exchange,
        routing_key="mykey",
        channel=conn,
        # message_ttl=600,
        # queue_arguments={
        #     "x-queue-type": "classic"
        # },
        durable=True
    )
    queue2.declare()


    class MyConsumer1(bootsteps.ConsumerStep):
        def get_consumers(self, channel):
            return [
                    kombu.Consumer(
                        channel,
                        queues=[queue1],
                        callbacks=[self.handle],
                        accept=["json"]
                )
            ]

        def handle(self, body, message):
            print(f"\n### 1 ###\nBODY: {body}\nMESSAGE: {message}\n#########\n")
            message.ack()


    class MyConsumer2(bootsteps.ConsumerStep):
        def get_consumers(self, channel):
            return [
                kombu.Consumer(
                    channel,
                    queues=[queue2],
                    callbacks=[self.handle],
                    accept=["json"]
                )
            ]

        def handle(self, body, message):
            print(f"\n### 2 ###\nBODY: {body}\nMESSAGE: {message}\n#########\n")
            message.ack()


    app.steps["consumer"].add(MyConsumer1)
    app.steps["consumer"].add(MyConsumer2)
