from django.contrib import admin

from .models import CoverLetterTemplate
from .models import ResumeTemplate


admin.site.register(CoverLetterTemplate)
admin.site.register(ResumeTemplate)
