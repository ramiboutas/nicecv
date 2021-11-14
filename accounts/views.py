from django.views.generic import TemplateView


class MyAccountView(TemplateView):
    template_name = 'account/my_account.html'




# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.shortcuts import redirect
#
# @login_required
# def set_paid_until_view(request, months):
#     user = request.user
#     user.set_paid_until(months)
#     messages.info(request, "You paid the pro for {months} months. Thank you!")
#     return redirect('home')
