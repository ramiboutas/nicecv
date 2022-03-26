from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Resume
from utils.files import delete_path_file


@receiver(post_delete, sender=Resume)
def delete_resumes(sender, instance, **kwargs):
    """
    Delete resume files
    """
    try:
        delete_path_file(instance.image.path)
        delete_path_file(instance.pdf.path)
    except:
        pass



# from .tasks import create_resume_file_objects
# from profiles.models import Profile, Skill, Language, Education, Experience, Certification, Course, Honor, Organization, Patent, Project, Publication, Volunteering

# @receiver(post_delete, sender=Skill)
# @receiver(post_save, sender=Skill)
# @receiver(post_delete, sender=Language)
# @receiver(post_save, sender=Language)
# @receiver(post_delete, sender=Education)
# @receiver(post_save, sender=Education)
# @receiver(post_delete, sender=Experience)
# @receiver(post_save, sender=Experience)
# @receiver(post_delete, sender=Certification)
# @receiver(post_save, sender=Certification)
# @receiver(post_delete, sender=Course)
# @receiver(post_save, sender=Course)
# @receiver(post_delete, sender=Honor)
# @receiver(post_save, sender=Honor)
# @receiver(post_delete, sender=Organization)
# @receiver(post_save, sender=Organization)
# @receiver(post_delete, sender=Patent)
# @receiver(post_save, sender=Patent)
# @receiver(post_delete, sender=Project)
# @receiver(post_save, sender=Project)
# @receiver(post_delete, sender=Publication)
# @receiver(post_save, sender=Publication)
# @receiver(post_delete, sender=Volunteering)
# @receiver(post_save, sender=Volunteering)
# @receiver(post_save, sender=Profile)
# def file_creation_trigger(sender, instance, **kwargs):
#     if sender == Profile:
#         create_resume_file_objects.delay(pk=instance.pk)
#     else:
#         create_resume_file_objects.delay(pk=instance.profile.pk)
