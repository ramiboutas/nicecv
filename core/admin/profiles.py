from django.contrib import admin

from ..models import cvs
from ..models import profiles


class SkillInline(admin.TabularInline):
    model = profiles.Skill
    extra = 0


class CvInline(admin.TabularInline):
    model = cvs.Cv
    extra = 0


class LanguageInline(admin.TabularInline):
    model = profiles.LanguageAbility
    extra = 0


class EducationInline(admin.StackedInline):
    model = profiles.Education
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = profiles.Experience
    extra = 0


class AchievementInline(admin.TabularInline):
    model = profiles.Achievement
    extra = 0


class ProjectInline(admin.TabularInline):
    model = profiles.Project
    extra = 0


class PublicationInline(admin.TabularInline):
    model = profiles.Publication
    extra = 0


@admin.register(profiles.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category", "lang", "created"]
    list_filter = ["category", "public", "lang", "created"]
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
