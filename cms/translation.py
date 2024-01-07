from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models.setttings import Banner, Legal
from .models.snippets import FrequentAskedQuestion


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ("title", "text", "linked_page")


# FAQs
@register(FrequentAskedQuestion)
class FrequentAskedQuestionTranslationOptions(TranslationOptions):
    fields = ("question", "answer")


# Legal
@register(Legal)
class LegalTranslationOptions(TranslationOptions):
    fields = ("privacy_policy_page", "terms_page", "impress_page")
