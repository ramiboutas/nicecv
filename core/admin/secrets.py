from django.contrib import admin

from ..models.secrets import Secrets

# Register your models here.


@admin.register(Secrets)
class SecretAdmin(admin.ModelAdmin):
    list_display = ["name"]
