from io import StringIO

from django.core.management import call_command

from config.test import TestCase


class LoadInitDataTests(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "load_init_data",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_objs_created(self):
        out = self.call_command()
        self.assertEqual(out, "Objects created.\n")
