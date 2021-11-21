from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import EarlyAdopter, NewsletterSubscriber
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    models = CustomUser
    list_display = ['email', 'username', 'has_paid', ]
    fieldsets = (
        (None, {'fields': ('username', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),  # added "age" field
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'paid_until')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EarlyAdopter)
admin.site.register(NewsletterSubscriber)
