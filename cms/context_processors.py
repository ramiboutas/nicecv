from functools import cache
from itertools import chain


from wagtail.models import Locale
from cms.models.blog import BlogIndexPage
from cms.models.flex import FlexPage
from cms.models.text import TextPage


@cache
def cms_menu_pages(request):
    try:
        locale = Locale.objects.get(language_code=request.LANGUAGE_CODE)
    except Locale.DoesNotExist:
        return {"cms_navbar_pages": None, "cms_footer_pages": None}
    blog_pages = BlogIndexPage.objects.filter(locale=locale, show_in_menus=True)
    flex_pages = FlexPage.objects.filter(locale=locale, show_in_menus=True)
    text_pages = TextPage.objects.filter(locale=locale, show_in_menus=True)
    return {
        "cms_navbar_pages": chain(blog_pages, flex_pages),
        "cms_footer_pages": chain(blog_pages, flex_pages, text_pages),
    }
