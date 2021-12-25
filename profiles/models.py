from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.utils import timezone

import uuid
from PIL import Image
# from croppie.fields import CroppieField

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.username.id, filename)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    imported_from_linkedin = models.BooleanField(default=False) # set in

    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile

    # address       Localizable address that a member wants to display on the profile. Represented as a MultiLocaleString object type.
    # birthDate     Birth date of the member. Represented as a date object.
    # firstName 	Localizable first name of the member. Represented as a MultiLocaleString object
    # geoLocation 	Member's location listed in their profile; may be null if no location is selected.
    #               GeoUrn defined by standardization is used to specify the location.
    # headline      Localizable headline of member's choosing. Represented as a MultiLocaleString object type.

    address = models.CharField(null=True, blank=True, max_length=100)
    birth_date = models.DateTimeField(null=True, blank=True)
    first_name = models.CharField(null=True, blank=True, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    maiden_name = models.CharField(null=True, blank=True, max_length=50)
    geo_location = models.CharField(null=True, blank=True, max_length=100)
    headline = models.CharField(null=True, blank=True, max_length=100) # summary?
    linkedin_id = models.BigIntegerField(null=True, blank=True)
    linkedin_industry_id = models.BigIntegerField(null=True, blank=True)
    linkedin_last_modified = models.DateTimeField(null=True, blank=True)

    # Linkedin API can give multiple phone numbers (take one: priority 1.MOBILE 2.HOME 3.WORK)
    # https://docs.microsoft.com/en-us/linkedin/shared/references/v2/profile/phone-number
    phone = models.CharField(null=True, blank=True, max_length=200)


    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='profiles/', default='profiles/defaultphoto.png') # change later when auth is finneshed
    fullname = models.CharField(max_length=200)
    jobtitle = models.CharField(max_length=200)
    birthdate = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    interests = models.CharField(max_length=200)

    # labels
    skill_label = models.CharField(max_length=100, default=_('Skills'))
    experience_label = models.CharField(max_length=100, default=_('Work experience'))
    education_label = models.CharField(max_length=100, default=_('Education'))
    publication_label = models.CharField(max_length=100, default=_('Publications'))


    def __str__(self):
        return f"{self.name} {self.id} "

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.photo)

        if img.height > 300 or img.width > 300:
            new_size = (300, 300) # image proportion is manteined / we dont need to do extra work
            img.thumbnail(new_size)
            img.save(self.photo.path)


class BackgroundPicture(models.Model):
    """
    Metadata about the member's background image in the profile. This replaces existing backgroundImage.
    See Background Picture Fields for a description of the fields available within this object.
    """
    profile = models.ForeignKey(Profile, related_name='background_picture', on_delete=models.CASCADE)
    linkedin_data = models.JSONField(null=True, blank=True)


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
    linkedin_data = models.JSONField(null=True, blank=True) # include all the fields

    linkedin_id = models.BigIntegerField(null=True, blank=True)
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
    linkedin_data = models.JSONField(null=True, blank=True)

    linkedin_id = models.BigIntegerField(null=True, blank=True)
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
    linkedin_data = models.JSONField(null=True, blank=True)

    linkedin_id = models.BigIntegerField(null=True, blank=True)
    degree_name = models.CharField(null=True, blank=True, max_length=100)
    program = models.CharField(null=True, blank=True, max_length=100)
    start_date = models.CharField(null=True, blank=True, max_length=50)
    end_date = models.CharField(null=True, blank=True, max_length=50)
    school_name = models.CharField(null=True, blank=True, max_length=100)
    organization = models.CharField(null=True, blank=True, max_length=100)
    activities = models.CharField(null=True, blank=True, max_length=200)
    notes = models.CharField(null=True, blank=True, max_length=200) # use as description
    grade = models.CharField(null=True, blank=True, max_length=20)

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
    linkedin_data = models.JSONField(null=True, blank=True)

    linkedin_id = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=200)
    issue_date = models.CharField(null=True, blank=True, max_length=100)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    occupation = models.CharField(null=True, blank=True, max_length=100)


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

    linkedin_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.CharField(null=True, blank=True, max_length=200)
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
    linkedin_id = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=100)
    inventors = models.CharField(null=True, blank=True, max_length=200)
    pending = models.BooleanField(null=True, blank=True)
    issuer = models.CharField(null=True, blank=True, max_length=100)
    issue_date = models.CharField(null=True, blank=True, max_length=100) # when pending = False
    application_number = models.IntegerField(null=True, blank=True) # when pending = True
    description = models.CharField(null=True, blank=True, max_length=300)
    filling_date = models.CharField(null=True, blank=True, max_length=100) # when pending = True
    number = models.IntegerField(null=True, blank=True) # when pending = False
    url = models.URLField(null=True, blank=True)



class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=200)
    level = models.IntegerField(default=50)

    def __str__(self):
        return self.title




class Publication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    date = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    begin = models.CharField(max_length=20)
    end = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title
