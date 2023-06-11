from django.contrib import admin

from .models import FreePlan
from .models import PremiumPlan
from .models import PlanFAQ

admin.site.register(PremiumPlan)
admin.site.register(FreePlan)
admin.site.register(PlanFAQ)
