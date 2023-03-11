from modeltranslation.translator import register, TranslationOptions

from .models import Plan
from .models import PlanFAQ



@register(Plan)
class PlanTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(PlanFAQ)
class PlanFAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)