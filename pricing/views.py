from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import OrderForm

class PricingView(FormView):
    template_name = 'pricing/plan_list.html'
    # form_class = OrderForm
    # success_url = reverse_lazy('order_plan')


class OrderView(FormView, LoginRequiredMixin):
    template_name = 'pricing/order.html'
