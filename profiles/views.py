from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from django.utils.translation import gettext as _

from .models import Profile
User = get_user_model()

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect']=self['Location']
    status_code = 200


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/profile_update.html'
    model = Profile
    fields = '__all__'
    # exclude = ['candidate_name','candidate_position','candidate_email', 'candidate_phone','candidate_location', 'candidate_website']
    def get_object(self):
        obj = get_object_or_404(Profile, pk=self.kwargs['pk'], user=self.request.user)
        return obj

class ProfileCreateView(LoginRequiredMixin, CreateView):
    template_name = 'profiles/profile_update.html'
    model = Profile
    fields = '__all__'
    def form_valid(self, form):
        response = super(ProfileCreateView, self).form_valid(form)
        trigger_client_event(response, 'ObjectCreatedEvent', { },)
        return response


# htmx - profile - create object
@login_required
@require_POST
def hx_create_object_view(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    object = Profile(user=request.user, first_name=first_name, last_name=last_name, email=email)
    object.save()
    # once the object is created, we redirect the user to the obj update url
    return HTTPResponseHXRedirect(redirect_to=object.get_update_url())
