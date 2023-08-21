from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from ..forms.users import CustomUserChangeForm
from ..models.users import User


@login_required
def account_dashboard(request):
    return render(request, "account/account_dashboard.html")


@login_required
def account_edit(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, _("Account updated"))
        else:
            messages.error(request, _("An error occurred"))

    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "account/account_edit.html", context)


@login_required
def redirect_change_password(request, id):
    try:
        user = User.objects.get(id=id)
        if user == request.user:
            return redirect("account_change_password")
    except User.DoesNotExist:
        pass

    messages.error(request, _("An error occurred"))
    return redirect("/")
