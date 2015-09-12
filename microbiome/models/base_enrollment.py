from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG
from edc_constants.constants import NOT_APPLICABLE

from .maternal_consent import MaternalConsent


class BaseEnrollment(BaseUuidModel):

    """Base Model for antenal and postnatal enrollment"""

    maternal_consent = models.OneToOneField(
        MaternalConsent,
        verbose_name="Mother'\s Consent")

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time of Enrollment",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    verbal_hiv_status = models.CharField(
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

    valid_regime = models.CharField(
        verbose_name="(Interviewer) If HIV +VE, do records show that participant takes ARV'\s?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=("Valid regimes include: Atripla, Truvada-Efavirenz or Tenofovir, "
                   "Entricitibine-Efavirenz, Truvad-Lamivudine-Efavirenz. If NO, participant"
                   "will not be enrolled"))

    process_rapid_test = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=('Remember, rapid test is for HIV -VE, UNTESTED, UNKNOWN, REFUSED-to-ANSWER'
                   'verbal responses'))

    date_of_rapid_test = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        blank=True)

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True,)

    class Meta:
        abstract = True
