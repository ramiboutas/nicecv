from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import PlanFAQ
from .models import PremiumPlan


@register(PremiumPlan)
class PlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(PlanFAQ)
class PlanFAQTranslationOptions(TranslationOptions):
    fields = (
        "question",
        "answer",
    )
