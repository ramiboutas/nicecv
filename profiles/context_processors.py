# from tex.models import TexTemplate
from django.conf import settings


# These template context variables will be available in the whole app
def profile_variables(request):
    return {
        # 'profile_website_choices': settings.PROFILE_WEBSITE_CHOICES,
        'profile_language_level_choices': settings.PROFILE_LANGUAGE_LEVEL_CHOICES,

        # text max_length (for db & html forms)
        'max_length_super_short': settings.TEXT_MAX_LENGTH_SUPER_SHORT,
        'max_length_short': settings.TEXT_MAX_LENGTH_SHORT,
        'max_length_normal': settings.TEXT_MAX_LENGTH_NORMAL,
        'max_length_large': settings.TEXT_MAX_LENGTH_LARGE,
        'max_length_super_large': settings.TEXT_MAX_LENGTH_SUPER_LARGE,

        'request': request
    }
