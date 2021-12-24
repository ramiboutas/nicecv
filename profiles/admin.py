from django.contrib import admin

# Register your models here.


from .models import Profile, Certification, Course


admin.site.register(Profile)
admin.site.register(Certification)
admin.site.register(Course)
