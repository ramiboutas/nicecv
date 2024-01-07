from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models.setttings import Banner, Brand, Legal
from .models.menus import CustomFlatMenu, CustomFlatMenuItem, CustomMainMenuItem
from .models.snippets import FrequentAskedQuestion


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


# LEgal
@register(Legal)
class LegalTranslationOptions(TranslationOptions):
    fields = ("privacy_policy_page", "terms_page", "impress_page")
