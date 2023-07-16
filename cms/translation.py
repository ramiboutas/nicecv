from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import CustomMainMenuItem
from .models import CustomFlatMenuItem
from .models import CustomFlatMenu


@register(CustomMainMenuItem)
class MainMenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)


@register(CustomFlatMenuItem)
class FlatMenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)


@register(CustomFlatMenu)
class FlatMenuTranslationOptions(TranslationOptions):
    fields = ("heading",)
