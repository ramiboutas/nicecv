import multiprocessing
import os
import sys

from django.core.management.commands import test


class Command(test.Command):
    def __init__(self, *args, **kwargs):
        if sys.platform == "darwin":
            # macOS workaround
            # Workaround for https://code.djangoproject.com/ticket/31169
            os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
            if multiprocessing.get_start_method(allow_none=True) != "fork":
                multiprocessing.set_start_method("fork")
        super().__init__(*args, **kwargs)
