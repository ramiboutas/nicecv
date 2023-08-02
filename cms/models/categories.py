from wagtail.models import Page


class CategoryPage(Page):
    template = "cms/category_page.html"
    parent_page_type = ["cms.HomePage"]
    subpage_types = ["cms.TextPage", "cms.FlexPage"]
