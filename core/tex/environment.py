from jinja2 import Environment

from .filters import FILTERS


def environment(**options):
    """ "  This code is a copy from https://github.com/weinbusch/django-tex"""
    options.update(
        {
            "autoescape": None,
            "extensions": ["core.tex.extensions.GraphicspathExtension"],
        }
    )
    env = Environment(**options)
    env.filters = FILTERS
    return env
