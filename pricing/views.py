from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded


# there is no url for this view, use admin interface for that.
def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'pricing/payment.html',
                            {'form': form, 'payment': payment})



class PricingListView(ListView):
    template_name = 'pricing/list.html'
