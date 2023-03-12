from django.contrib import admin

from .models import Order
from .models import PremiumPlan

admin.site.register(PremiumPlan)
admin.site.register(Order)
