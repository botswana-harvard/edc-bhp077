from django_crypto_fields.fields import FirstnameField, IdentityField
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.apps import apps
try:
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from edc_base.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future, dob_not_future)
from edc_constants.choices import YES_NO, GENDER
from edc_registration.models import RegisteredSubject

from ..choices import (CHECKLIST_DISEASES, HIVRESULT_CHOICE, PREG_DELIVERED_CHOICE)


class MaternalEligibilityPre (BaseUuidModel):
    """A model completed by the user that confirms basic eligibility. Before or after delivery."""

    registered_subject = models.OneToOneField(
        RegisteredSubject,
        help_text=''
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility'
    )

    first_name = FirstnameField(
        verbose_name='First name',
        validators=[RegexValidator("^[A-Z]{1,250}$", "Ensure first name is in CAPS and "
                                   "does not contain any spaces or numbers")],
        help_text="")

    initials = models.CharField(
        verbose_name='Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Z]{1,3}$", "Must be Only CAPS and 2 or 3 letters. No spaces or numbers allowed.")],
        help_text=""
    )

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[dob_not_future, ],
        help_text="Format is YYYY-MM-DD."
    )

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER
    )

    has_identity = models.CharField(
        verbose_name="[Interviewer] Has the subject presented a valid OMANG or other identity document?",
        max_length=10,
        choices=YES_NO,
        help_text='Allow Omang, Passport number, driver\'s license number or Omang receipt number. '
                  'If \'NO\' participant will not be enrolled.'
    )

    identity = IdentityField(
        verbose_name="Identity number (OMANG, etc)",
        unique=True,
        null=True,
        blank=True,
        help_text="Use Omang, Passport number, driver's license number or Omang receipt number"
    )


#     identity_type = IdentityTypeField(
#         null=True)
    identity_type = models.CharField(
        blank=True,
        max_length=10,
        null=True
    )

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO,
        help_text=""
    )

    # TODO: turn this field in to a ManyToMany.
    disease = models.CharField(
        verbose_name="Do you currently have any of the following diseases?",
        max_length=15,
        help_text="If participant has any of the diseases, then not eligible.",
        choices=CHECKLIST_DISEASES
    )

    currently_pregnant = models.CharField(
        verbose_name="Is the participant still pregnant or has already delivered?",
        max_length=30,
        choices=PREG_DELIVERED_CHOICE,
        help_text=''
    )

    pregnancy_weeks = models.IntegerField(
        verbose_name='If pregnant, how many weeks in to the pregnancy?',
        help_text='Must be at least 36 weeks pregnant.'
    )

    verbal_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        max_length=30,
        choices=HIVRESULT_CHOICE,
        help_text=''
    )

    evidence_pos_hiv_status = models.BooleanField(
        verbose_name="(Interviewer) If HIV+, have you seen evidence of the HIV result?",
        default=False,
        help_text='Evidence of HIV positive status either by showing a positive testing result or '
                  'showing IDCC records that demonstrate that she is taking ARVs.'
    )

    rapid_test_result = models.CharField(
        verbose_name="(Interviewer: Only for those without HIV+ documentation.) What is the rapid test result?",
        max_length=30,
        choices=HIVRESULT_CHOICE,
        help_text='If mother has no evidence of HIV status or has not tested on or after 32 weeks gestational age, '
                  'she must undergo  rapid testing. If positive, will not have been on treatment sufficiently long '
                  'enough and is not eligible.  If negative, eligible to join the study.'
    )

    internal_identifier = models.CharField(
        max_length=36,
        null=True,
        default=None,
        editable=False,
        help_text='Identifier to track registered subject between eligibility pre/post and consent'
    )

    def save(self, *args, **kwargs):
        SubjectConsent = get_model('microbiome', 'SubjectConsent')
        consent = SubjectConsent.objects.filter(maternal_eligibility_pre=self)
        if consent.exists() and consent[0].is_verified:
            raise TypeError('You can only edit eligibility if the maternal consent has not been verified yet')
        super(MaternalEligibilityPre, self).save(*args, **kwargs)

    @property
    def age_in_years(self):
        return relativedelta(timezone.now().date(), self.dob).years

    @property
    def is_eligible(self):
        """Evaluates the initial maternal eligibility criteria"""
        if not (self.age_in_years < 18):
            return False
        elif self.has_identity.lower() == 'no':
            return False
        elif self.citizen.lower() == 'no':
            return False
        elif self.disease.lower() != 'n/a':
            return False
        elif self.pregnancy_weeks < 36:
            return False
        elif self.verbal_hiv_status.lower() == 'neg' and self.rapid_test_result.lower() == 'pos':
            return False
        else:
            return True

    def get_create_registered_subject_post_save(self):
        # You need to call this in a post save because self.id is None when creating a new instance.
        if not self.internal_identifier:
            self.internal_identifier = self.id
            try:
                # You want to use as few values as possible here that will guarantee
                # uniqueness, so that data cleaning doesnt break the function.
                registered_subject = RegisteredSubject.objects.get(
                    registration_identifier=self.internal_identifier)
            except RegisteredSubject.DoesNotExist:
                # No consent yet, so cannot record dob, identity etc.
                registered_subject = RegisteredSubject.objects.create(
                    created=self.created,
                    first_name=self.first_name,
                    initials=self.initials,
                    gender=self.gender,
                    subject_type='subject',
                    registration_identifier=self.internal_identifier,
                    registration_datetime=self.created,
                    user_created=self.user_created,
                    registration_status='study_potential'
                )
            # set registered_subject for this
            self.registered_subject = registered_subject
            # Because we are using self.internal_identifier, this method will only be exercuted once.
            # You do not have to worry about calling save in a post save signal method.
            self.save()

    def __str__(self):
        return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Eligibility Pre"
        verbose_name_plural = "Maternal Eligibility Pre"
