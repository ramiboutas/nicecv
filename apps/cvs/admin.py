from django.contrib import admin

from .models import Cv


@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    list_display = ["profile", "tex"]
