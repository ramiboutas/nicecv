from django.contrib import admin

from .models import Certification
from .models import Course
from .models import Education
from .models import Experience
from .models import Honor
from .models import Language
from .models import Organization
from .models import Patent
from .models import Profile
from .models import Project
from .models import Publication
from .models import Resume
from .models import Skill
from .models import Volunteering

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Course)
admin.site.register(Certification)
admin.site.register(Honor)
admin.site.register(Organization)
admin.site.register(Patent)
admin.site.register(Project)
admin.site.register(Publication)
admin.site.register(Volunteering)
######################################
admin.site.register(Resume)
