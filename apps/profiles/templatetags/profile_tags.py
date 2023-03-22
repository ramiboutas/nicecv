from django import template

register = template.Library()


@register.simple_tag
def call_child_method(obj, method_name, klass, *args, **kwargs):
    method = getattr(obj, method_name)
    return method(klass, *args, **kwargs)
