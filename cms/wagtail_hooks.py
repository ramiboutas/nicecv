from .models.snippets import Person

from wagtail.snippets.views.snippets import SnippetViewSet


class PersonViewSet(SnippetViewSet):
    model = Person
    menu_label = "People"  # ditch this to use verbose_name_plural from model
    icon = "group"  # change as required
    list_display = ("name", "job_title", "thumb_image")
    list_filter = {
        "job_title": ["icontains"],
    }
