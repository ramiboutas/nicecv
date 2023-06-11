from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import Language


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)
