from django.contrib import admin

from ..models.cvs import Cv


@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    list_display = ["profile", "tex", "pdf_time", "image_time", "rendering_time"]
    list_filter = ["profile__category", "tex", "profile__language_setting"]
    readonly_fields = ["pdf_time", "image_time", "rendering_time", "image", "pdf"]
