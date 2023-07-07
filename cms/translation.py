from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from wagtailmenus.models import MainMenuItem


@register(MainMenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)
