from django.conf import settings
from jinja2 import nodes
from jinja2.ext import Extension


def format_path_for_latex(path):
    """ "  This code is a copy from https://github.com/weinbusch/django-tex"""
    if not isinstance(path, str):
        path = str(path)

    path = path.replace("\\", "/")
    if not path.endswith("/"):
        path += "/"
    if " " in path:
        path = '"' + path + '"'
    path = "{" + path + "}"
    return path


class GraphicspathExtension(Extension):
    """

    This code is a copy from https://github.com/weinbusch/django-tex

    Adds a `graphicspath` tag to Jinja2 that
    prints out a \\graphicspath{ {<path>} } command, where
    <path> is derived from the LATEX_GRAPHICSPATH setting or
    the BASE_DIR setting by default.

    """

    tags = {"graphicspath"}

    def parse(self, parser):
        list_of_paths = getattr(settings, "LATEX_GRAPHICSPATH", [settings.BASE_DIR])
        value = (
            "\\graphicspath{ "
            + " ".join(map(format_path_for_latex, list_of_paths))
            + " }"
        )
        node = nodes.Output(lineno=next(parser.stream).lineno)
        node.nodes = [nodes.MarkSafe(nodes.Const(value))]
        return node
