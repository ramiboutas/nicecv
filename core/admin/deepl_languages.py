from django.contrib import admin

from ..models.deepl_language import DeeplLanguage

# Register your models here.


@admin.register(DeeplLanguage)
class DeeplLanguageAdmin(admin.ModelAdmin):
    list_filter = [
        "is_source",
        "is_target",
        "supports_formality",
    ]
    list_display = ["name", "code"] + list_filter
    fields = [f.name for f in DeeplLanguage._meta.get_fields()]
