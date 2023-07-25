from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def svg(svgfile, css_class=""):
    return mark_safe(svgfile.read().decode())
