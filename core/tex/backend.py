from django.template.backends.jinja2 import Jinja2


class TeXEngine(Jinja2):
    app_dirname = "templates"
