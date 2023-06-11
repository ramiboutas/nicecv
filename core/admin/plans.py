from django.contrib import admin

from ..models.plans import FreePlan
from ..models.plans import PremiumPlan
from ..models.plans import PlanFAQ

admin.site.register(PremiumPlan)
admin.site.register(FreePlan)
admin.site.register(PlanFAQ)
