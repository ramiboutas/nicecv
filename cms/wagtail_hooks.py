from wagtail.snippets.views.snippets import SnippetViewSet

from .models.snippets import Person


class PersonViewSet(SnippetViewSet):
    model = Person
    menu_label = "People"
    icon = "group"
    list_display = ("name", "job_title", "thumb_image")
    list_filter = {"job_title": ["icontains"]}
