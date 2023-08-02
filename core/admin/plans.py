from django.contrib import admin

from ..models.plans import FreePlan
from ..models.plans import PremiumPlan

admin.site.register(PremiumPlan)
admin.site.register(FreePlan)
