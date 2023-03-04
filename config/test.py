from __future__ import annotations

from django.test.runner import DiscoverRunner
from django.test.utils import override_settings


class TestRunner(DiscoverRunner):
    def run_tests(self, *args, **kwargs):
        with override_settings(**TEST_SETTINGS):
            return super().run_tests(*args, **kwargs)

    @classmethod
    def add_arguments(self, parser):
        super().add_arguments(parser)

        # Modify parallel option to default to number of CPU cores
        # Find the action as already created in super(), and change its
        # 'default' (1) to its 'const' (the number of CPU cores)
        parallel_action = next(
            a for a in parser._optionals._actions if a.dest == "parallel"
        )
        parallel_action.default = parallel_action.const


TEST_SETTINGS = {
    "PAGE_SIZE": 10,  # Remove if not necessary
    "DEBUG": False,
    "USE_POSTGRES": True,
}
