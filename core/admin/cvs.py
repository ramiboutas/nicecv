from django.contrib import admin

from ..models.cvs import Cv


@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    list_display = ["profile", "tex"]
    list_filter = ["profile__category", "profile__language_setting"]
