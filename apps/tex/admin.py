from django.contrib import admin

from .models import CoverLetterTemplate
from .models import Tex


admin.site.register(CoverLetterTemplate)
admin.site.register(Tex)
