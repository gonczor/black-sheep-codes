from courses.tasks import test_task


def cover_image_resize_callback(sender, *args, **kwargs):
    test_task.apply_async()
