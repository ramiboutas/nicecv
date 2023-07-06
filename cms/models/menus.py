from wagtailmenus.models import AbstractMainMenu
from wagtailmenus.models import AbstractMainMenuItem

from wagtail.models import Page
from wagtail.models import ParentalKey

from django.db import models
from wagtailmenus.conf import settings

# LocalizedMainMenu and LocalizedMainMenuItem:
# https://github.com/jazzband/wagtailmenus/issues/242#issuecomment-795138779


class LocalizedMainMenu(AbstractMainMenu):
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
                and item.link_page.depth >= settings.SECTION_ROOT_DEPTH
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


class LocalizedMainMenuItem(AbstractMainMenuItem):
    menu = ParentalKey(
        LocalizedMainMenu,
        on_delete=models.CASCADE,
        related_name=settings.MAIN_MENU_ITEMS_RELATED_NAME,
    )

    def __init__(self, *args, **kwargs):
        """
        This makes the menu work seamlessly with multi-language entirely:
        - In the admin you only add the pages once per language, but the
          menu also appears even if you are visiting the page that is in
          another language.
        - The menu item's text is in the current language.
        - The menu item's link point to the right language.
        """
        super().__init__(*args, **kwargs)
        if self.link_page and self.link_page.localized:
            self.link_page = self.link_page.localized
