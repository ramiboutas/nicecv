from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models.plans import PremiumPlan


@register(PremiumPlan)
class PlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")
