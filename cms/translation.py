from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import Banner
from .models import Brand
from .models import CustomFlatMenu
from .models import CustomFlatMenuItem
from .models import CustomMainMenuItem
from .models import FrequentAskedQuestion


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
@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ("footer_text",)


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ("title", "text", "linked_page")


# FAQs
@register(FrequentAskedQuestion)
class FrequentAskedQuestionTranslationOptions(TranslationOptions):
    fields = ("question", "answer")
