import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.utils import stacktrace
from aws_xray_sdk.ext.util import construct_xray_header, inject_trace_header
from celery import signals
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


def xray_before_task_publish(**kwargs):
    task_name = kwargs.get('sender')
    headers = kwargs.get('headers', {})
    body = kwargs.get('body', {})
    task_id = headers.get('id') or body.get('id')  # Celery 3/4 support

    subsegment = xray_recorder.begin_subsegment(
        name=task_name,
        namespace='remote',
    )

    if subsegment is None:
        # Not in segment
        return

    subsegment.put_metadata('task_id', task_id, namespace='celery')

    if headers:
        inject_trace_header(headers, subsegment)


def xray_after_task_publish(**kwargs):
    xray_recorder.end_subsegment()


def xray_task_prerun(**kwargs):
    task = kwargs.get('sender')
    task_id = kwargs.get('task_id')

    xray_header = construct_xray_header({})

    segment = xray_recorder.begin_segment(
        name=task.name,
        traceid=xray_header.root,
        parent_id=xray_header.parent,
    )
    segment.save_origin_trace_header(xray_header)
    segment.put_metadata('task_id', task_id, namespace='celery')


def xray_task_postrun(**kwargs):
    xray_recorder.end_segment()


def xray_task_failure(**kwargs):
    einfo = kwargs.get('einfo')
    segment = xray_recorder.current_segment()
    if einfo:
        stack = stacktrace.get_stacktrace(limit=xray_recorder._max_trace_back)
        segment.add_exception(einfo.exception, stack)


def connect_celery_signal_receivers():
    signals.task_prerun.connect(xray_task_prerun)
    signals.task_postrun.connect(xray_task_postrun)
    signals.task_failure.connect(xray_task_failure)
    signals.before_task_publish.connect(xray_before_task_publish)
    signals.after_task_publish.connect(xray_after_task_publish)


connect_celery_signal_receivers()
