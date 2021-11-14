from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render

from .forms import SelectMonthPlanForm, LifeTimePlanForm
from .models import Plan


def update_price(request):
    months = request.GET.get('months')
    plan = Plan.objects.filter(months=int(months)).first()
    context = {'plan': plan}
    return render(request, 'pricing/partials/price_months.html', context)
