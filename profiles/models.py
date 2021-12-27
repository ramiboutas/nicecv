from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django.utils import timezone

import uuid
from PIL import Image
# from croppie.fields import CroppieField

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.username.id, filename)

class Profile(models.Model):
    """
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    location = models.CharField(null=True, blank=True, max_length=100)
    birth_date = models.DateTimeField(null=True, blank=True)

    first_name = models.CharField(null=True, blank=True, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    maiden_name = models.CharField(null=True, blank=True, max_length=50)

    # media
    picture = models.ImageField(null=True, blank=True, upload_to='profiles/')

    jobtitle = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)

    linkedin_id = models.BigIntegerField(null=True, blank=True)
    linkedin_industry_id = models.BigIntegerField(null=True, blank=True)
    linkedin_last_modified = models.DateTimeField(null=True, blank=True)
    linkedin_vanity_name = models.CharField(null=True, blank=True, max_length=100) # www.linkedin.com/in/{vanityName}

    # contact info
    phone = models.CharField(null=True, blank=True, max_length=200)
    website = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    interests = models.CharField(max_length=200)

    # labels
    skill_label = models.CharField(max_length=100, default=_('Skills'))
    position_label = models.CharField(max_length=100, default=_('Work experience'))
    education_label = models.CharField(max_length=100, default=_('Education'))
    publication_label = models.CharField(max_length=100, default=_('Publications'))
    project_label = models.CharField(max_length=100, default=_('Projects'))
    project_label = models.CharField(max_length=100, default=_('Publications'))


    def __str__(self):
        return f"{self.name} {self.id} "

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.photo)

        if img.height > 300 or img.width > 300:
            new_size = (300, 300) # image proportion is manteined / we dont need to do extra work
            img.thumbnail(new_size)
            img.save(self.photo.path)


class Certification(models.Model):
    """
    An object representing the certifications that the member holds.
    See Certification Fields for a description of the fields available within this object.

    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/certification

    # id 	            Yes The unique identifer of the certification object.
    # startMonthYear 	No 	Start date for the certification. It is a  Date  type. Does not support "day" field.
    # endMonthYear 	    No 	End date for the certification. It is a  Date  type. Does not support "day" field.
    # name 	            No 	Localizable certification name. It is a  MultiLocaleString  type.
    # authority         No 	Localizable name of the certification's issuing body. It is a  MultiLocaleString  type.
    # company 	        No 	Standardized referenced company URN.
    # licenseNumber     No 	Localizable license number for the certification. It is a  MultiLocaleString  type.
    # url 	            No 	External reference to the certification's website or program.

    """
    profile = models.ForeignKey(Profile, related_name='certifications', on_delete=models.CASCADE)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField(null=True, blank=True, max_length=100)
    authority = models.CharField(null=True, blank=True, max_length=100)
    company = models.CharField(null=True, blank=True, max_length=100)
    license = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)


class Course(models.Model):
    """
    An object representing courses the member has taken.
    See Course Fields for a description of the fields available within this object.

    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/course
    # id            Yes The unique identifier of the course object.
    # name          No 	Localizable certification name. It is a  MultiLocaleString  type.
    # number 	    No 	Assigned course number. Represented in string.
    # occupation    No 	Member's occupation when the course was completed. Standardized referenced company or school URN.
    """
    profile = models.ForeignKey(Profile, related_name='courses', on_delete=models.CASCADE)
    name = models.JSONField(null=True, blank=True)
    number = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)

class Education(models.Model):
    """
    An object representing the member's educational background.
    See Education Fields for a description of the fields available within this object.

    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/education

    id                  Yes The unique identifier of the education object.
    degreeName          No 	Localizable degree attained at this school. MultiLocaleString type.
    program             No 	Standardized referenced school program URN.
    startMonthYear 	  	No 	Start date of the education. It is a Date type. Does not support "day" and "month" field.
    endMonthYear        No 	End date of the education. It is a Date type. Does not support "day" and "month" field.
    schoolName          No 	Localizable school name. It is a MultiLocaleString type.
    organization 		No 	Organization URN used to represent a school.
    activities          No 	Localizable description of activities, societies, clubs... MultiLocaleString type.
    notes               No  Localizable description for additional details about this education. It is a MultiLocaleRichText type.
    grade               No 	Grade attained in the area of study.
    - grade             No 	Localizable grade of the degree or major. It is a MultiLocaleString type.
    fieldsOfStudy       No 	Degrees achieved in respective fields of study.
    - fieldOfStudyName 	No 	Localizable field of study or major. It is a MultiLocaleString type.
    memberRichContents  No 	The list of MemberRichContentUrn associated with the education. Default to empty array.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    degree_name = models.CharField(null=True, blank=True, max_length=100)
    program = models.CharField(null=True, blank=True, max_length=100)
    grade = models.CharField(null=True, blank=True, max_length=20)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    school_name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=300)

    def __str__(self):
        return self.degree_name


class Honor(models.Model):
    """
    An object representing the various honors and awards the member has received. See Honor Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/honor

    # id          Yes 	The unique identifier of the honor object.
    # description No 	Localizable description of the honor or award. It is a  MultiLocaleRichText  type.
    # issueDate   No 	Month and year the honor or award was issued. It is a  Date  type. Does not support "day" field.
    # issuer      No 	Localizable entity that issued the honor or award. It is a  MultiLocaleString  type.
    # occupation  No 	Member's occupation when the honor or award was completed
    # title       Yes Localizable title of the honor or award. It is a  MultiLocaleString  type.

    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='honors')
    title = models.CharField(null=True, blank=True, max_length=100)
    issue_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)


class Organization(models.Model):
    """
    An object representing the organizations that the member is in.
    See Organization Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/organization

    # id                Yes The unique identifier of the organization object.
    # name              No 	Localizable name of the organization. It is a  MultiLocaleString  type.
    # description       No 	Localizable description for the position held at the organization. It is a  MultiLocaleRichText  type.
    # startMonthYear    No 	Start date for the certification. It is a  Date  type. Does not support "day" field.
    # endMonthYear      No 	Month and year start date at the organization. It is a  Date  type. Does not support "day" field.
    # occupation        No 	Member's occupation when the course was completed. Standardized referenced company or school URN.
    # position          No 	Localizable name of the position at the organization. It is a  MultiLocaleString  type.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organizations')
    linkedin_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    position = models.CharField(null=True, blank=True, max_length=100)


class Patent(models.Model):
    """
    An object representing the various patents associated with the member.
    See Patent Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/patent

    # id                Yes The unique identifier of the patent object.
    # title             Yes Localizable title of the patent. It is a  MultiLocaleString  type.
    # inventors 	  	Yes Members who created the patent or contributed to it. Array of Contributors.
    # - memberId        No 	The inventor represented in person URN.
    # - name            No 	Localizable member name. It is a  MultiLocaleString  type.
    # pending           Yes The status of patent represented as a boolean.
    # issuer            Yes Localizable issuer of the patent. Issuer based on country (ISO-3166). MultiLocaleString type.
    # issueDate 	  	No 	Month, day, and year the patent was officially issued. Displayed when pending is false.
    # applicationNumber No 	Localizable patent application number. MultiLocaleString  type. Displayed when pending is true.
    # description 	  	No 	Localizable description for additional details about this education. It is a  MultiLocaleRichText  type.
    # filingDate 	  	No 	Month, day, and year the patent was filed. It is a  Date  type. Only displayed when pending is true.
    # number            No 	Localizable patent number. It is a  MultiLocaleString  type. Only displayed when pending is false.
    # url               No 	URL referencing the patent represented in string.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patents')
    linkedin_id = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=100)
    inventors = models.CharField(null=True, blank=True, max_length=200)
    pending = models.BooleanField(null=True, blank=True)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    issue_date = models.CharField(null=True, blank=True, max_length=100) # when pending = False
    application_number = models.IntegerField(null=True, blank=True) # when pending = True
    description = models.TextField(null=True, blank=True)
    filling_date = models.CharField(null=True, blank=True, max_length=100) # when pending = True
    number = models.IntegerField(null=True, blank=True) # when pending = False
    url = models.URLField(null=True, blank=True)



class Position(models.Model):
    """
    Employment history. See Positions for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/position

    # id                      Yes   The unique identifier of the position object.
    # company                 No    Standardized referenced company URN.
    # companyName             No 	Localizable company name as entered by the member. It is a MultiLocaleString type.
    # title                   No 	Localizable title name of the position. It is a MultiLocaleString type.
    # description             No 	Localizable description for this position. MultiLocaleRichText type.
    # startMonthYear          No 	Start month and year at this position. It is a Date type. Does not support "day" field.
    # endMonthYear            No 	Last month and year at this position. Missing value means the position is current.
    # locationName            No 	Legacy localizable location name of the position. It is a MultiLocaleString type.
    # location                No 	Legacy location for the position. Only displayed if locationName field is empty.
    #  - countryCode          Yes   2 letter country code. Refer to the standardized country URNs for more information.
    #  - regionCode           No    Optional integer code. Refer to the standardized region URNs for more information.
    # memberRichContents      No 	The list of MemberRichContentUrn associated with the education. Default to empty array.
    # geoPositionLocation     No 	New location of the position member worked or works at.
    #  - displayLocationName  Yes   Location of the position as selected from typeahead or entered by the member.
    #                               This field is a MultiLocaleString type. Validations enforced are:
    #                               1) the keys in a localized map all exist within the profile's supportedLocale set;
    #                               2) there is a value for profile default locale in the localized string maps.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    company_name = models.CharField(null=True, blank=True, max_length=100)
    location_name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return self.title



class Project(models.Model):
    """
    An object representing the various projects associated with the member.
    See Project Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/project

    # id                Yes The unique identifier of the publication object.
    # title             Yes Localizable name of the project. It is a  MultiLocaleString  type.
    # description       No  Localizable description of the project. It is a  MultiLocaleRichText  type.
    # startMonthYear    No  Start date for the certification. It is a  Date  type. Does not support "day" field.
    # endMonthYear      No  Month and year indicating when the project ended. It is a  Date  type. Does not support "day" field.
    # members           Yes People who contributed to the project. Represented in an array of Contributors
    # occupation        No  Position a member held while working on this project. Standardized referenced company or school URN.
    # singleDate        No  A boolean type: Ongoing project without an end date or a project with start & end dates.
    # url               No  URL referencing the project represented in string.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    members = models.CharField(null=True, blank=True, max_length=200)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    ongoing = models.BooleanField(null=True, blank=True) # singleDate
    issuer = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title



class Publication(models.Model):
    """
    An object representing the various publications associated with the member.
    See Publication Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/publication

    # id            Yes The unique identifier of the publication object.
    # name          Yes Localizable name of the publication. It is a  MultiLocaleString  type.
    # date          No 	Day, month, and year indicating when the publication was published. It is a  Date  type.
    # description   No 	Localizable description of the publication. It is a  MultiLocaleRichText  type.
    # authors       Yes People who wrote the publication or contributed to it. Represented in an array of Contributors.
    # publisher     No  Localizable publication or publisher for the title. It is a  MultiLocaleString  type.
    # url           No  URL referencing the publication represented in string.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    name = models.CharField(null=True, blank=True, max_length=200)
    date = models.CharField(null=True, blank=True, max_length=20)
    description = models.TextField(null=True, blank=True, max_length=1000)
    authors = models.CharField(null=True, blank=True, max_length=200)
    publisher = models.CharField(null=True, blank=True, max_length=100)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name




class Skill(models.Model):
    """
    An object representing the skills that the member holds.
    See Skill Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/skill

    # id    Yes 	The unique identifier of the skill object.
    # name  Yes 	Localizable skill name as defined by the member. It is a  MultiLocaleString  type.

    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)
    level = models.IntegerField(default=50) # Linkedin does not include this

    def __str__(self):
        return self.name




class VolunteeringExperience(models.Model):
    """
    An object representing the member's volunteering experience.
    See Volunteering Experience Fields for a description of the fields available within this object.

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/volunteering-experience

    # id                Yes The unique identifier of the volunteering experience object.
    # company           No 	Standardized referenced company URN.
    # startMonthYear    No 	Month and year start date of the experience. It is a  Date  type. Does not support "day" field.
    # endMonthYear      No 	Month and year end date of the experience. It is a  Date  type. Does not support "day" field.
    # companyName       Yes Localizable company name. It is a  MultiLocaleString  type.
    # description       No 	Localizable description of the experience. It is a  MultiLocaleRichText  type.
    # cause             No 	Cause of the volunteering experience represented in predefined string.
    # role              Yes Localizable duty or responsibility performed at this volunteering experience. MultiLocaleString  type.
    # singleDate        No 	A boolean type: Ongoing volunteering experience or volunteering experience with start & end dates.

    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteering_experiences')
    title = models.CharField(null=True, blank=True, max_length=100)
    role = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=100)
    end_date = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True, max_length=1000)
    cause = models.CharField(null=True, blank=True, max_length=100)
    ongoing = models.BooleanField(null=True, blank=True) # singleDate




class Website(models.Model):
    """
    Localized websites the member wants displayed on the profile.
    See Website Fields for a description of the fields available within this object.
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/website
    """
    WEBSITE_CHOICES =  [
        ('Linkedin', 'Linkedin'),
        ('Github', 'Github'),
        ('Twitter', 'Twitter'),
        ('Youtube', 'Youtube'),
        ('Other', _('Other')),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='linkedin_websites')
    category = models.CharField(null=True, blank=True, max_length=100, choices=WEBSITE_CHOICES)
    label = models.CharField(null=True, blank=True, max_length=100) # if other > label
    url = models.URLField(null=True, blank=True)
