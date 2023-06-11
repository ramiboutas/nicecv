from django.contrib import admin

# Register your models here.

from ..models.secrets import Secrets


@admin.register(Secrets)
class SecretAdmin(admin.ModelAdmin):
    list_display = ["name"]
