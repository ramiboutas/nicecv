from django.contrib import admin


from ..models.tex import CvTex


@admin.register(CvTex)
class CvTexAdmin(admin.ModelAdmin):
    list_display = ["__str__", "template_name", "average_rendering_time", "downloads"]

    readonly_fields = [
        "title",
        "slug",
        "template_name",
        "interpreter",
        "license",
        "credits",
        "credits_url",
        "downloads",
    ]
