from wagtail.models import Page


from ..blocks import ArticleStreamBlock


class BlogIndexPage(Page):
    template = "cms/blog_index.html"


class BlogPost(Page):
    template = "cms/blog_post.html"

    body = ArticleStreamBlock()
