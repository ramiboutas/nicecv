from django.contrib import admin

from .models import FreePlan
from .models import PremiumPlan

admin.site.register(PremiumPlan)
admin.site.register(FreePlan)
