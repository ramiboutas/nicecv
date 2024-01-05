from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from ..forms.users import CustomUserChangeForm
from ..forms.users import CustomUserCreationForm


from ..models.users import UserPremiumPlan


class UserPremiumPlanInline(admin.TabularInline):
    model = UserPremiumPlan
    extra = 0


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    models = get_user_model()
    list_display = ("__str__", "email", "username", "asked_to_verify_email")
    fieldsets = (
        (
            None,
            {"fields": ("username", "password", "asked_to_verify_email")},
        ),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "avatar_url")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )
    inlines = (UserPremiumPlanInline,)


@admin.register(UserPremiumPlan)
class UserPremiumPlanAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "plan")
    list_filter = ("plan", "user")
