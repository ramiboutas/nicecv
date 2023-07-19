from django.core.exceptions import ValidationError
from django.urls import reverse
from wagtail.management.commands.fixtree import Command as FixTreeCommand
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from wagtail.models import Page

from .home import HomePage
from .home import get_default_homepage


class PureDjangoPage(Page):
    """A way to access to the core app urls (first level paths: no slash in between)
    * Valid: /profiles/                    slug = "profiles" (it will work)
    * Not valid: /profiles/detailed/       slug = "profiles-detailed" (it won't work)
    """

    # the instances shouldn't be served by wagtail
    template = "404.html"

    # content_panels = []
    # promote_panels = []

    @classmethod
    def update_objects(cls):
        cls.objects.all().delete()
        FixTreeCommand().handle()
        home = get_default_homepage()

        if not home:
            return

        pages = [
            cls(
                title="Profile List",
                slug=reverse("profile_list").replace("/", ""),
                show_in_menus=True,
            ),
            cls(
                title="Profile create",
                slug=reverse("profile_create").replace("/", ""),
                show_in_menus=True,
            ),
            cls(
                title="Plan List",
                slug=reverse("plan_list").replace("/", ""),
                show_in_menus=True,
            ),
            cls(
                title="User dashboard",
                slug=reverse("user_dashboard").replace("/", ""),
                show_in_menus=True,
            ),
            cls(
                title="User signup",
                slug=reverse("account_signup").replace("/", ""),
                show_in_menus=True,
            ),
            cls(
                title="User login",
                slug=reverse("account_login").replace("/", ""),
                show_in_menus=True,
            ),
            cls(
                title="User logout",
                slug=reverse("account_logout").replace("/", ""),
                show_in_menus=True,
            ),
        ]
        for page in pages:
            try:
                home.add_child(instance=page)
            except AttributeError:
                pass
            except ValidationError:
                pass
        home.save()

    def __str__(self):
        return self.title + " (Generated)"
