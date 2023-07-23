from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import CustomMainMenuItem
from .models import CustomFlatMenuItem
from .models import CustomFlatMenu
from .models import FooterSlogan


# menus
@register(CustomMainMenuItem)
class MainMenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)


@register(CustomFlatMenuItem)
class FlatMenuItemTranslationOptions(TranslationOptions):
    fields = ("link_text",)


@register(CustomFlatMenu)
class FlatMenuTranslationOptions(TranslationOptions):
    fields = ("heading",)


# site setttings
@register(FooterSlogan)
class FooterSloganLinksTranslationOptions(TranslationOptions):
    fields = ("text",)