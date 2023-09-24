from django.core.exceptions import ValidationError
from django.urls import reverse
from wagtail.admin.panels import FieldPanel
from wagtail.management.commands.fixtree import Command as FixTreeCommand
from wagtail.models import Page

from .home import get_default_homepage


class DjangoServedPage(Page):
    """A way to access to the core app urls (first level paths: no slash in between)
    * Valid: /profiles/                    slug = "profiles" (it will work)
    * Not valid: /profiles/detailed/       slug = "profilesdetailed" (it won't work)
    """

    # the instances shouldn't be served by wagtail
    template = "404.html"

    subpage_types = []
    parent_page_type = ["wagtailcore.Page"]

    content_panels = [
        FieldPanel("title"),
        FieldPanel("show_in_menus"),
        FieldPanel("slug", read_only=True),
    ]
    promote_panels = []

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
                slug=reverse("account_dashboard").replace("/", ""),
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
            except AttributeError as e:
                print(e)
            except ValidationError as e:
                print(e)
        home.save()

    def __str__(self):
        return self.title + " (Generated)"
