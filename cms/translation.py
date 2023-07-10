from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import CustomMainMenuItem


@register(CustomMainMenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)


# @register()
