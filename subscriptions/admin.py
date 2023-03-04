from django.contrib import admin

from .models import Order
from .models import Plan

admin.site.register(Plan)
admin.site.register(Order)
