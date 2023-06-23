from django.contrib import admin

from ..models.tex import Tex


@admin.register(Tex)
class CvTexAdmin(admin.ModelAdmin):
    list_display = ["__str__", "template_name", "average_rendering_time", "downloads"]

    readonly_fields = [
        "title",
        "slug",
        "template_name",
        "interpreter",
        "license",
        "credits",
        "source_url",
        "downloads",
    ]
