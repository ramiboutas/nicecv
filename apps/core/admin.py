from django.contrib import admin

# Register your models here.
from .models import Language
from .models import Setting


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ["name"]
