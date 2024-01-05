from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models.plans import PremiumPlan, FreePlan


@register(PremiumPlan)
class PremiumPlanTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(FreePlan)
class FreePlanTranslationOptions(TranslationOptions):
    fields = ("name",)
