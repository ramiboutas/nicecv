from django.contrib import admin
from . import models

from apps.cvs.models import Cv


class SkillInline(admin.TabularInline):
    model = models.Skill
    extra = 0


class CvInline(admin.TabularInline):
    model = Cv
    extra = 0


class LanguageInline(admin.TabularInline):
    model = models.Language
    extra = 0


class EducationInline(admin.StackedInline):
    model = models.Education
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = models.Experience
    extra = 0


class AchievementInline(admin.TabularInline):
    model = models.Achievement
    extra = 0


class ProjectInline(admin.TabularInline):
    model = models.Project
    extra = 0


class PublicationInline(admin.TabularInline):
    model = models.Publication
    extra = 0


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category", "language_setting", "created"]
    list_filter = ["category", "public", "language_setting", "created"]
    inlines = [
        CvInline,
        SkillInline,
        LanguageInline,
        EducationInline,
        ExperienceInline,
        AchievementInline,
        ProjectInline,
        PublicationInline,
    ]
