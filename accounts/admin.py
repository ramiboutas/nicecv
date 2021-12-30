from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    models = CustomUser
    list_display = ['email', 'username', 'has_paid', ]
    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar_url',)}),
        (_('Premium'), {'fields': ('paid_until', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
