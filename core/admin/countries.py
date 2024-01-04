from django.contrib import admin

from ..models.countries import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "gdp", "currency", "wikipedia_url")
    list_filter = ("currency",)
