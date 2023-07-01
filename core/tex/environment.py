from jinja2 import Environment

from .filters import FILTERS


def environment(**options):
    options.update(
        {
            "autoescape": None,
            "extensions": ["core.tex.extensions.GraphicspathExtension"],
        }
    )
    env = Environment(**options)
    env.filters = FILTERS
    return env
