from django.contrib import admin

from .models import Plan
from .models import Order

admin.site.register(Plan)
admin.site.register(Order)
