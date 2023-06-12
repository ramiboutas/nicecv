from django.contrib import admin


from ..models.tex import CvTex


@admin.register(CvTex)
class CvTexAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "average_rendering_time",
    ]
