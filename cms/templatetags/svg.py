from django import template
from django.utils.safestring import mark_safe


register = template.Library()


ERROR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
</svg>
"""


@register.simple_tag
def svg(svgfile, **kwargs):
    css_class = kwargs.get("class", None)

    try:
        content = svgfile.read().decode()
    except (AttributeError, Exception):
        content = ERROR_SVG

    if css_class:
        index = content.find(" ")
        content = content[:index] + f' class="{css_class}"' + content[index:]

    return mark_safe(content)
