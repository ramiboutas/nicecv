from django.contrib import admin

from ..models.tex import Tex


@admin.action(description="Make Premium")
def set_premium(modeladmin, request, queryset):
    queryset.update(is_premium=True)


@admin.action(description="Make Free")
def set_free(modeladmin, request, queryset):
    queryset.update(is_premium=False)


@admin.action(description="Activate")
def activate(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.action(description="Deactivate")
def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.register(Tex)
class CvTexAdmin(admin.ModelAdmin):
    actions = [set_premium, set_free, activate, deactivate]
    list_display = (
        "__str__",
        "template_name",
        "average_rendering_time",
        "downloads",
        "is_premium",
        "active",
    )

    readonly_fields = (
        "category",
        "name",
        "title",
        "template_name",
        "interpreter",
        "license",
        "credits",
        "source_url",
        "downloads",
    )

    list_filter = ("is_premium", "active")
