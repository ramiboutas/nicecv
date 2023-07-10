from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from modelcluster.fields import ParentalKey
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel


from wagtailmenus.conf import settings as wagtailmenus_settings
from wagtailmenus.panels import FlatMenuItemsInlinePanel
from wagtailmenus.models import AbstractFlatMenu, AbstractFlatMenuItem
from wagtailmenus.models import AbstractMainMenu, AbstractMainMenuItem


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

    @property
    def menu_text(self):
        """Use `translated_link_text` instead of just `link_text`"""
        return self.translated_link_text or getattr(
            self.link_page,
            wagtailmenus_settings.PAGE_FIELD_FOR_MENU_ITEM_TEXT,
            self.link_page.title,
        )

    # Also override the panels attribute, so that the new fields appear
    # in the admin interface
    panels = (
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("url_append"),
        FieldPanel("link_text"),
        FieldPanel("handle"),
        FieldPanel("allow_subnav"),
    )


class CustomMainMenu(AbstractMainMenu):
    def get_pages_for_display(self):
        """Returns a queryset of all pages needed to render the menu."""
        if hasattr(self, "_raw_menu_items"):
            # get_top_level_items() may have set this
            menu_items = self._raw_menu_items
        else:
            menu_items = self.get_base_menuitem_queryset()

        # Start with an empty queryset, and expand as needed
        queryset = Page.objects.none()

        for item in (item for item in menu_items if item.link_page):
            if item.link_page.localized:
                item.link_page = item.link_page.localized

            if (
                item.allow_subnav
                and item.link_page.depth >= wagtailmenus_settings.SECTION_ROOT_DEPTH
            ):
                # Add this branch to the overall `queryset`
                queryset = queryset | Page.objects.filter(
                    path__startswith=item.link_page.path,
                    depth__lt=item.link_page.depth + self.max_levels,
                )
            else:
                # Add this page only to the overall `queryset`
                queryset = queryset | Page.objects.filter(id=item.link_page_id)

        # Filter out pages unsutable display
        queryset = self.get_base_page_queryset() & queryset

        # Always return 'specific' page instances
        return queryset.specific()


from django.conf import settings


for translated, _ in settings.WAGTAIL_CONTENT_LANGUAGES:
    pass


class CustomMainMenuItem(AbstractMainMenuItem):
    menu = ParentalKey(
        CustomMainMenu,  # we can use the model from above
        on_delete=models.CASCADE,
        related_name=settings.WAGTAILMENUS_MAIN_MENU_ITEMS_RELATED_NAME,
    )
    panels = (
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("url_append"),
        FieldPanel("link_text"),
        FieldPanel("link_text_en"),
        FieldPanel("link_text_es"),
        FieldPanel("handle"),
        FieldPanel("allow_subnav"),
    )
