from django.contrib import admin

from ..models.languages import Language

# Register your models here.


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_filter = [
        "is_source_in_deepl",
        "is_target_in_deepl",
        "supports_formality_in_deepl",
    ]
    list_display = ["name", "code"] + list_filter
    fields = [f.name for f in Language._meta.get_fields()].remove("profile")
