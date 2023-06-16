from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models.languages import Language
from .models.plans import PlanFAQ
from .models.plans import PremiumPlan


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(PremiumPlan)
class PlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(PlanFAQ)
class PlanFAQTranslationOptions(TranslationOptions):
    fields = (
        "question",
        "answer",
    )
