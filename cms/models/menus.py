from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from modelcluster.fields import ParentalKey
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel


from wagtailmenus.conf import settings as wagtailmenus_settings
from wagtailmenus.panels import FlatMenuItemsInlinePanel
from wagtailmenus.panels import MainMenuItemsInlinePanel
from wagtailmenus.models import AbstractFlatMenu, AbstractFlatMenuItem
from wagtailmenus.models import AbstractMainMenu, AbstractMainMenuItem


def get_localized_fieldpannels(field_name: str):
    return [
        FieldPanel(field_name + "_" + lang[0])
        for lang in settings.WAGTAIL_CONTENT_LANGUAGES
    ]


menu_item_panels = (
    [
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("url_append"),
        FieldPanel("link_text"),
    ]
    + get_localized_fieldpannels("link_text")
    + [
        FieldPanel("handle"),
        FieldPanel("allow_subnav"),
    ]
)


class CustomFlatMenu(AbstractFlatMenu):
    # Like pages, panels for menus are split into multiple tabs.
    # To update the panels in the 'Content' tab, override 'content_panels'
    # To update the panels in the 'Settings' tab, override 'settings_panels'
    content_panels = (
        MultiFieldPanel(
            heading=_("Settings"),
            children=(
                FieldPanel("title"),
                FieldPanel("site"),
                FieldPanel("handle"),
            ),
        ),
        MultiFieldPanel(
            heading=_("Heading"),
            children=(FieldPanel("heading"),),
            classname="collapsible",
        ),
        FlatMenuItemsInlinePanel(),
    )


class CustomFlatMenuItem(AbstractFlatMenuItem):
    """A custom menu item model to be used by ``FlatMenu``"""

    menu = ParentalKey(
        CustomFlatMenu,  # we can use the model from above
        on_delete=models.CASCADE,
        related_name=settings.WAGTAILMENUS_FLAT_MENU_ITEMS_RELATED_NAME,
    )
    panels = menu_item_panels


class CustomMainMenu(AbstractMainMenu):
    content_panels = (MainMenuItemsInlinePanel(),)


class CustomMainMenuItem(AbstractMainMenuItem):
    menu = ParentalKey(
        CustomMainMenu,
        on_delete=models.CASCADE,
        related_name=settings.WAGTAILMENUS_MAIN_MENU_ITEMS_RELATED_NAME,
    )
    panels = menu_item_panels
