from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel


from wagtailmenus.panels import FlatMenuItemsInlinePanel
from wagtailmenus.panels import MainMenuItemsInlinePanel
from wagtailmenus.models import AbstractFlatMenu, AbstractFlatMenuItem
from wagtailmenus.models import AbstractMainMenu, AbstractMainMenuItem

from ..utils import localized_fieldpanel_list


common_menu_item_panels = (
    [
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("url_append"),
        # FieldPanel("link_text"),
    ]
    + localized_fieldpanel_list("link_text")
    + [
        FieldPanel("handle"),
        # FieldPanel("allow_subnav"),
    ]
)

flat_menu_heading_panels = tuple(
    [
        # FieldPanel("heading"),
    ]
    + localized_fieldpanel_list("heading"),
)


class CustomFlatMenu(AbstractFlatMenu):
    # Like pages, panels for menus are split into multiple tabs.
    # To update the panels in the 'Content' tab, override 'content_panels'
    # To update the panels in the 'Settings' tab, override 'settings_panels'
    panels = (
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
            children=flat_menu_heading_panels,
            classname="collapsible",
        ),
        FlatMenuItemsInlinePanel(),
    )


class CustomFlatMenuItem(AbstractFlatMenuItem):
    """A custom flat menu item model to be used by ``CustomFlatMenu``"""

    menu = ParentalKey(
        CustomFlatMenu,  # we can use the model from above
        on_delete=models.CASCADE,
        related_name=settings.WAGTAILMENUS_FLAT_MENU_ITEMS_RELATED_NAME,
    )
    panels = common_menu_item_panels


class CustomMainMenu(AbstractMainMenu):
    """A custom main menu item model to be used by ``CustomMainMenu``"""

    content_panels = (MainMenuItemsInlinePanel(),)


class CustomMainMenuItem(AbstractMainMenuItem):
    menu = ParentalKey(
        CustomMainMenu,
        on_delete=models.CASCADE,
        related_name=settings.WAGTAILMENUS_MAIN_MENU_ITEMS_RELATED_NAME,
    )

    add_to_profile_dropdown = models.BooleanField(default=False)

    panels = common_menu_item_panels + [
        FieldPanel("add_to_profile_dropdown"),
    ]
