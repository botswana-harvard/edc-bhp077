from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils.translation import ugettext as _

from edc_base.model.fields import IdentityTypeField
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future, dob_not_future)
from edc_registration.models import RegisteredSubject

from django.db import models

from django_crypto_fields.fields import IdentityField, FirstnameField
from ..choices import (CHECKLIST_DISEASES, VERBALHIVRESULT_CHOICE, PREG_DELIVERED_CHOICE, YES_NO, GENDER)

from edc_base.models import BaseUuidModel


class EligibilityChecklist (BaseUuidModel):
    """A model completed by the user that confirms and saves eligibility
    information for potential participant."""

    registered_subject = models.OneToOneField(
        RegisteredSubject,
        null=True,
        blank=True,
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

#     first_name = FirstnameField(
#         verbose_name='First name',
#         validators=[RegexValidator("^[A-Z]{1,250}$", "Ensure first name is in CAPS and "
#                                    "does not contain any spaces or numbers")],
#         help_text="")
    first_name = models.CharField(
        verbose_name='First name',
        max_length=20,
        validators=[RegexValidator("^[A-Z]{1,250}$", "Ensure first name is in CAPS and "
                                   "does not contain any spaces or numbers")],
        help_text=""
    )

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
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD."
    )

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER
    )

    has_identity = models.CharField(
        verbose_name=_("[Interviewer] Has the subject presented a valid OMANG or other identity document?"),
        max_length=10,
        choices=YES_NO,
        help_text=_('Allow Omang, Passport number, driver\'s license number or Omang receipt number. '
                    'If \'NO\' participant will not be enrolled.')
    )

#     identity = IdentityField(
#         verbose_name=_("Identity number (OMANG, etc)"),
#         unique=True,
#         null=True,
#         blank=True,
#         help_text=("Use Omang, Passport number, driver's license number or Omang receipt number")
#         )
    identity = models.CharField(
        verbose_name=_("Identity number (OMANG, etc)"),
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Use Omang, Passport number, driver's license number or Omang receipt number")
    )

#     identity_type = IdentityTypeField(
#         null=True)
    identity_type = models.CharField(
        max_length=20,
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
        help_text=_("If participant has any of the diseases, then not eligible."),
        choices=CHECKLIST_DISEASES
    )

    pregnant_delivered = models.CharField(
        verbose_name=_("Is the participant still pregnant or has already delivered?"),
        max_length=30,
        choices=PREG_DELIVERED_CHOICE,
        help_text=''
    )

    gestation_weeks = models.IntegerField(
        verbose_name='If pregnant, how many weeks gestation?',
        null=True,
        blank=True,
        help_text='Must be at least 36 weeks pregnant.'
    )

    post_partum = models.IntegerField(
        verbose_name='If delivered, how many hours post-partum?',
        null=True,
        blank=True,
        help_text=_('Must be at less than 72 hours post-partum.')
    )

    verbal_hiv_status = models.CharField(
        verbose_name=_("Please tell me your current HIV status?"),
        max_length=30,
        choices=VERBALHIVRESULT_CHOICE,
        help_text=_('Evidence of HIV positive status either by showing a positive testing result or '
                    'showing IDCC records that demonstrate that she is taking ARVs.')
    )

    evidence_pos_hiv_status = models.BooleanField(
        verbose_name=_("(Interviewer) If HIV+, have you seen evidence of the HIV result?"),
        default=False,
        help_text=''
    )

    rapid_test_result = models.CharField(
        verbose_name=_("(Interviewer) What is the rapid test result?"),
        max_length=30,
        choices=VERBALHIVRESULT_CHOICE,
        help_text=_('If mother has no evidence of HIV status or has not tested on or after 32 weeks gestational age, '
                    'she must undergo  rapid testing.  If positive, will not have been on treatment sufficiently long '
                    'enough and is not eligible.  If negative, eligible to join the study.')
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(EligibilityChecklist, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    @property
    def age_in_years(self):
        return True

    class Meta:
        app_label = "microbiome"
        verbose_name = "Eligibility Checklist"
        verbose_name_plural = "Eligibility Checklist"
