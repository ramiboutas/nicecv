from __future__ import annotations

from importlib import import_module
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location

from django.test.runner import DiscoverRunner
from django.test.utils import override_settings


class TestRunner(DiscoverRunner):
    def run_tests(self, *args, **kwargs):
        with override_settings(**TEST_SETTINGS):
            return super().run_tests(*args, **kwargs)


TEST_SETTINGS = {
    "PAGE_SIZE": 10,  # Remove if not necessary
    "DEBUG": False,
}


def reimport_module(name):  # pragma: no cover
    """
    Reimport a module by name, and return a new, isolated module object.
    Based on recipe:
    https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    """
    original = import_module(name)
    spec = spec_from_file_location(f"_remiport_module.{name}", original.__file__)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
