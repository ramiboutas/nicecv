from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import CustomMainMenuItem
from .models import CustomFlatMenuItem


@register(CustomMainMenuItem)
class MainMenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)


@register(CustomFlatMenuItem)
class FlatMenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)
