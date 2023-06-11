from django.utils.safestring import mark_safe


from core.exceptions import ErrorBySettingFormFieldAttributes
from core.exceptions import ErrorBySettingFormWidgetInputType


def build_form_widgets(
    form: object,
    fields: list = [],
    widget_types: dict = {},
    html_class: str = None,
    html_autocomplete=None,
    html_rows: str = None,
    x_bind_class: str = None,
    hx_post: str = None,
    hx_trigger: str = None,
    hx_swap: str = None,
):
    # Gather all html and frontend attributes
    attrs = {}

    if html_class:
        # html class
        attrs = attrs | {"class": mark_safe(html_class)}

    if html_autocomplete:
        # HTML attribute: autocomplete
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
        attrs = attrs | {"autocomplete": mark_safe(html_autocomplete)}

    if x_bind_class:
        # alpinejs :class attr.
        attrs = attrs | {":class": mark_safe(x_bind_class)}

    if html_rows:
        attrs = attrs | {"rows": mark_safe(html_rows)}

    if hx_post:
        # htmx hx-post method
        attrs = attrs | {"hx-post": mark_safe(hx_post)}

    if hx_trigger:
        # htmx hx-trigger method
        attrs = attrs | {"hx-trigger": mark_safe(hx_trigger)}

    if hx_swap:
        # htmx hx-trigger method
        attrs = attrs | {"hx-swap": mark_safe(hx_swap)}

    # Set this attrs to the fields
    for field_name in fields:
        try:
            form.fields[field_name].widget.attrs.update(attrs)
        except ErrorBySettingFormFieldAttributes as e:
            e.add_note(f"Exception by setting attrs to the field {field_name}")
            raise e

    # Set widget types
    for field_name, input_type in widget_types.items():
        try:
            form.fields[field_name].widget.input_type = input_type
        except ErrorBySettingFormWidgetInputType as e:
            e.add_note(f"Exception by setting attrs to the field {field_name}")
            raise e
