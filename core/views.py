from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse("profiles_list"))
        return render(self.request, self.template_name)