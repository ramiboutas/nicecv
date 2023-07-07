from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtailmenus.conf import settings
from wagtailmenus.panels import FlatMenuItemsInlinePanel
from wagtailmenus.models import AbstractFlatMenu, AbstractFlatMenuItem


class TranslatedField(object):
    """
    A class that can be used on models to return a 'field' in the
    desired language, where there a multiple versions of a field to
    cater for multiple languages (in this case, English, German & French)
    """

    def __init__(self, en_field, de_field, fr_field):
        self.en_field = en_field
        self.de_field = de_field
        self.fr_field = fr_field

    def __get__(self, instance, owner):
        active_language = translation.get_language()
        if active_language == "de":
            return getattr(instance, self.de_field)
        if active_language == "fr":
            return getattr(instance, self.fr_field)
        return getattr(instance, self.en_field)


class TranslatedFlatMenu(AbstractFlatMenu):
    heading_de = models.CharField(
        verbose_name=_("heading (german)"),
        max_length=255,
        blank=True,
    )
    heading_fr = models.CharField(
        verbose_name=_("heading (french)"),
        max_length=255,
        blank=True,
    )
    translated_heading = TranslatedField("heading", "heading_de", "heading_fr")

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
            children=(
                FieldPanel("heading"),
                FieldPanel("heading_de"),
                FieldPanel("heading_fr"),
            ),
            classname="collapsible",
        ),
        FlatMenuItemsInlinePanel(),
    )


class TranslatedFlatMenuItem(AbstractFlatMenuItem):
    """A custom menu item model to be used by ``TranslatedFlatMenu``"""

    menu = ParentalKey(
        TranslatedFlatMenu,  # we can use the model from above
        on_delete=models.CASCADE,
        related_name=settings.FLAT_MENU_ITEMS_RELATED_NAME,
    )
    link_text_de = models.CharField(
        verbose_name=_("link text (german)"),
        max_length=255,
        blank=True,
    )
    link_text_fr = models.CharField(
        verbose_name=_("link text (french)"),
        max_length=255,
        blank=True,
    )
    translated_link_text = TranslatedField("link_text", "link_text_de", "link_text_fr")

    @property
    def menu_text(self):
        """Use `translated_link_text` instead of just `link_text`"""
        return self.translated_link_text or getattr(
            self.link_page, settings.PAGE_FIELD_FOR_MENU_ITEM_TEXT, self.link_page.title
        )

    # Also override the panels attribute, so that the new fields appear
    # in the admin interface
    panels = (
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("url_append"),
        FieldPanel("link_text"),
        FieldPanel("link_text_de"),
        FieldPanel("link_text_fr"),
        FieldPanel("handle"),
        FieldPanel("allow_subnav"),
    )
