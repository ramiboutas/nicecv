from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render

from .forms import SelectMonthPlanForm, LifeTimePlanForm
from .models import Plan


def pricing_view(request):
    default_plan = Plan.objects.filter(default=True).first()
    context = {'plan': default_plan}
    return render(request, 'pricing/plan_list.html', context)