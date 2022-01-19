# from tex.models import TexTemplate
from django.conf import settings


# These template context variables will be available in the whole app
def nicecv(request):
    return {
        # 'tex_templates': TexTemplate.objects.filter(is_active=True), # for tex_templates
        'site_name': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
