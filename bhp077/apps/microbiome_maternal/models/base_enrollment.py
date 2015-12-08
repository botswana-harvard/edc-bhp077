from django.db import models

from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)
from edc_base.model.validators import date_not_before_study_start, date_not_future

from edc_consent.models import RequiresConsentMixin

from edc_constants.choices import (POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO)
from edc_constants.constants import NOT_APPLICABLE, NO, YES

from .maternal_off_study_mixin import MaternalOffStudyMixin
from .maternal_eligibility import MaternalEligibility
from ..maternal_choices import LIVE_STILL_BIRTH


class BaseEnrollment(MaternalOffStudyMixin, BaseAppointmentMixin, RequiresConsentMixin, BaseUuidModel):

    """Base class for antenatal and postnatal enrollment models"""

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        default=NO,
        choices=YES_NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    on_tb_tx = models.CharField(
        verbose_name="Are you being treated for tubercolosis?",
        choices=YES_NO,
        default=NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    on_hypertension_tx = models.CharField(
        verbose_name='Are you being treated for hypertension?',
        choices=YES_NO,
        default=NO,
        help_text='INELIGIBLE if YES',
        max_length=3
    )

    will_breastfeed = models.CharField(
        verbose_name='Are you willing to breast-feed your child for a whole year?',
        choices=YES_NO,
        default=NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    will_remain_onstudy = models.CharField(
        verbose_name="Are you willing to remain in the study during the infants first year of life",
        choices=YES_NO,
        default=NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    week32_test = models.CharField(
        verbose_name="Have you tested for HIV on OR after 32 weeks gestational age?",
        choices=YES_NO,
        default=NO,
        max_length=3)

    week32_test_date = models.DateField(
        verbose_name="Date of Test",
        validators=[datetime_not_future, ],
        null=True,
        blank=True)

    week32_result = models.CharField(
        verbose_name="What was your result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    current_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        choices=POS_NEG_UNTESTED_REFUSAL,
        max_length=30,
        help_text=("if POS or NEG, ask for documentation."))

    evidence_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the HIV result?",
        max_length=15,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs. If NO, participant"
                   "will not be enrolled"))

    valid_regimen = models.CharField(
        verbose_name="(Interviewer) If HIV +VE, do records show that participant takes ARV'\s?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=("Valid regimes include: Atripla, Truvada-Efavirenz or Tenofovir, "
                   "Entricitibine-Efavirenz, Truvad-Lamivudine-Efavirenz. If NO, participant"
                   "will not be enrolled"))

    valid_regimen_duration = models.CharField(
        verbose_name="Has the participant been on the regimen for a valid period of time?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=("If not 6 or more weeks then not eligible."))

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=('Remember, rapid test is for HIV -VE, UNTESTED, UNKNOWN, REFUSED-to-ANSWER'
                   'verbal responses'))

    rapid_test_date = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        validators=[
            date_not_before_study_start,
            date_not_future, ],
        blank=True)

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True,)

    gestation_wks = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        help_text=" (weeks of gestation). Eligible if >=36 weeks",
        null=True,
        blank=True,)

    antenatal_eligible = models.BooleanField(
        editable=False)

    postpartum_days = models.IntegerField(
        verbose_name="How many days postpartum?",
        help_text="If more than 3days, not eligible",
        null=True,
        blank=True,)

    vaginal_delivery = models.CharField(
        verbose_name="Was this a vaginal delivery?",
        choices=YES_NO,
        max_length=3,
        help_text="INELIGIBLE if NO")

    gestation_to_birth_wks = models.IntegerField(
        verbose_name="How many weeks after gestation was the child born?",
        help_text="ineligible if premature or born before 37weeks",
        null=True,
        blank=True,)

    delivery_status = models.CharField(
        verbose_name="Was this a live or still birth?",
        choices=LIVE_STILL_BIRTH,
        max_length=15,
        help_text='if still birth, not eligible')

    antenatal_enrollemet_eligible = models.NullBooleanField(
        editable=False)

    postnatal_enrollemet_eligible = models.NullBooleanField(
        editable=False)

    live_infants = models.IntegerField(
        verbose_name="How many live infants?",
        null=True,
        blank=True)

    enrollment_type = models.CharField(max_length=20)

    def maternal_eligibility_pregnant_yes(self):
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=self.get_subject_identifier(),
                currently_pregnant=YES,
            )
        except MaternalEligibility.DoesNotExist:
            return False
        return True

    def maternal_eligibility_pregnant_currently_delivered_yes(self):
        try:
            return MaternalEligibility.objects.get(
                registered_subject__subject_identifier=self.get_subject_identifier(),
                recently_delivered=YES,
            )
        except MaternalEligibility.DoesNotExist:
            return False
        return True

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def __unicode__(self):
        return "{0} {1}".format(
            self.registered_subject.subject_identifier,
            self.registered_subject.first_name)

    class Meta:
        abstract = True
