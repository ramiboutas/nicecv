from django.forms import ModelForm

from .models import Order


class SelectMonthPlanForm(ModelForm):

    class Meta:
        model = Order
        exclude = ('user', 'created', )

class LifeTimePlanForm(ModelForm):

    class Meta:
        model = Order
        exclude = ('user', 'created', )
