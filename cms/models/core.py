from wagtail.models import Page
from wagtail.management.commands.fixtree import Command as FixTreeCommand
from django.urls import reverse
from django.core.exceptions import ValidationError

from . import HomePage


class CorePage(Page):
    """A way to access to the core app urls (first level paths: no slash in between)
    * Valid: /profiles/                    slug = "profiles" (it will work)
    * Not valid: /profiles/detailed/       slug = "profiles-detailed" (it won't work)
    """

    # the instances shouldn't be served by wagtail
    template = "404.html"

    content_panels = []
    promote_panels = []

    @classmethod
    def update_objects(cls):
        cls.objects.all().delete()
        FixTreeCommand().handle()
        home = HomePage.objects.all().first()

        if not home:
            return

        core_pages = [
            cls(
                title="Profile List",
                slug=reverse("profile_list").replace("/", ""),
            ),
            cls(
                title="Profile create",
                slug=reverse("profile_create").replace("/", ""),
            ),
            cls(
                title="Plan List",
                slug=reverse("plan_list").replace("/", ""),
            ),
            cls(
                title="User dashboard",
                slug=reverse("user_dashboard").replace("/", ""),
            ),
        ]
        for core_page in core_pages:
            try:
                home.add_child(instance=core_page)
            except AttributeError:
                pass
            except ValidationError:
                pass
        home.save()

    def __str__(self):
        return self.title + " (Generated)"
