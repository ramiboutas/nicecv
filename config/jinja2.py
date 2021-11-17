from jinja2 import Environment
from django_htmx.jinja import django_htmx_script


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            # ...
            "django_htmx_script": django_htmx_script,
        }
    )
    return env
