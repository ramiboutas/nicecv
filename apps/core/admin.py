from django.contrib import admin

# Register your models here.
from .models import Language
from .models import Settings


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_filter = [
        "is_source_in_deepl",
        "is_target_in_deepl",
        "supports_formality_in_deepl",
        "use_in_faker",
    ]
    list_display = ["name", "code"] + list_filter


@admin.register(Settings)
class SettingAdmin(admin.ModelAdmin):
    list_display = ["name"]
