import inspect

from . import models
from . import forms


def get_profile_children():
    class_objs = [
        cls_obj
        for _, cls_obj in inspect.getmembers(models)
        if (inspect.isclass(cls_obj) and (models.AbstractChild in cls_obj.__bases__))
    ]
    return class_objs


def create_initial_profile(request) -> models.Profile:
    # TODO: move to utils.py
    fullname = ""
    email = ""
    if request.user:
        fullname = request.user.first_name + " " + request.user.last_name
        email = request.user.email

        profile = models.Profile.objects.create(user=request.user)
    else:
        profile = models.Profile.objects.create()

    # Add children objects
    ChildKlasses = get_profile_children()
    for ChildKlass in ChildKlasses:
        ChildKlass.objects.create(profile=profile)

    profile.fullname.text = fullname
    profile.email.text = email
    profile.fullname.save()
    profile.email.save()
    return profile


def collect_profile_context(profile) -> dict:
    context = {
        "fullname": forms.FullnameForm(instance=profile.fullname),
        "jobtitle": forms.JobtitleForm(instance=profile.jobtitle),
        "location": forms.LocationForm(instance=profile.location),
        "phone": forms.PhoneForm(instance=profile.phone),
        "email": forms.EmailForm(instance=profile.email),
        "website": forms.WebsiteForm(instance=profile.website),
        "description": forms.DescriptionForm(instance=profile.description),
    }
    return context
