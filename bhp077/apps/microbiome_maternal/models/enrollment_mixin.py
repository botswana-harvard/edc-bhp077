from django.db import models
from django.core.exceptions import ValidationError

from edc_base.model.validators import date_not_before_study_start, date_not_future
from edc_constants.choices import POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO, NO
from edc_constants.constants import NOT_APPLICABLE, YES, POS, NEG, NEVER, UNKNOWN, DWTA, SEROCONVERSION, IND


class EnrollmentMixin(models.Model):

    """Base Model for antenal and postnatal enrollment"""

    is_eligible = models.BooleanField(
        editable=False)

    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        # default=NO,
        choices=YES_NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    on_tb_tx = models.CharField(
        verbose_name="Are you being treated for tubercolosis?",
        choices=YES_NO,
        # default=NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    on_hypertension_tx = models.CharField(
        verbose_name='Are you being treated for hypertension?',
        choices=YES_NO,
        # default=NO,
        help_text='INELIGIBLE if YES',
        max_length=3)

    will_breastfeed = models.CharField(
        verbose_name='Are you willing to breast-feed your child for a whole year?',
        choices=YES_NO,
        # default=NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    will_remain_onstudy = models.CharField(
        verbose_name="Are you willing to remain in the study during the infants first year of life",
        choices=YES_NO,
        # default=NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    week32_test = models.CharField(
        verbose_name="Have you tested for HIV on OR after 32 weeks gestational age?",
        choices=YES_NO,
        default=NO,
        max_length=3)

    week32_test_date = models.DateField(
        verbose_name="Date of HIV Test",
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
        # default=NOT_APPLICABLE,
        choices=YES_NO_NA,
        help_text=("evidence = clinic and/or IDCC records. check regimes/drugs. If NO, participant"
                   "will not be enrolled"))

    valid_regimen = models.CharField(
        verbose_name="(Interviewer) If HIV +VE, do records show that participant takes ARV'\s?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        # default=NOT_APPLICABLE,
        max_length=15,
        help_text=("Valid regimes include: Atripla, Truvada-Efavirenz or Tenofovir, "
                   "Entricitibine-Efavirenz, Truvad-Lamivudine-Efavirenz. If NO, participant"
                   "will not be enrolled"))

    valid_regimen_duration = models.CharField(
        verbose_name="Has the participant been on the regimen for a valid period of time?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        # default=NOT_APPLICABLE,
        max_length=15,
        help_text=("If not 6 or more weeks then not eligible."))

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        # default=NOT_APPLICABLE,
        max_length=15,
        help_text=(
            'Remember, rapid test is for NEG, UNTESTED, UNKNOWN and Don\'t want to answer.'))

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
        blank=True)

    def __unicode__(self):
        return "{0} {1}".format(
            self.registered_subject.subject_identifier,
            self.registered_subject.first_name)

    def enrollment_hiv_status(self):
        """Returns the maternal HIV status at enrollment based on valid combinations
        expected from the form otherwise raises a ValueError.

        Note: the ValueError should never be excepted!!"""

        enrollment_hiv_status = None
        if self.evidence_hiv_status == YES:
            enrollment_hiv_status = self._hiv_status_with_evidence()
        elif self.evidence_hiv_status in [NO, NOT_APPLICABLE]:
            enrollment_hiv_status = self._hiv_status_with_without_evidence()
        if not enrollment_hiv_status:
            raise ValueError(
                'Unable to determine maternal hiv status at enrollment. '
                'Got current_hiv_status={}, evidence_hiv_status={}, '
                'rapid_test_done={}, rapid_test_result={}'.format(
                    self.current_hiv_status,
                    self.evidence_hiv_status,
                    self.rapid_test_done,
                    self.rapid_test_result))
        return enrollment_hiv_status

    def _hiv_status_with_evidence(self):
        """Returns the hiv status if evidence is available or None."""
        hiv_status_with_evidence = None
        if self.evidence_hiv_status == YES:
            if self.hiv_status_on_or_after_32wk() == POS:
                hiv_status_with_evidence = POS
            elif self.hiv_status_on_or_after_32wk() == NEG:
                hiv_status_with_evidence = NEG
            elif self.current_hiv_status == POS and self.rapid_test_done in [NO, NOT_APPLICABLE]:
                hiv_status_with_evidence = POS
            elif (self.current_hiv_status == POS and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status_with_evidence = POS
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == NEG):
                hiv_status_with_evidence = NEG
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == POS):
                hiv_status_with_evidence = SEROCONVERSION
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == IND):
                hiv_status_with_evidence = IND
        return hiv_status_with_evidence

    def _hiv_status_with_without_evidence(self):
        """Returns the hiv status if evidence is not available or None."""
        if self.evidence_hiv_status in [NO, NOT_APPLICABLE]:
            if (self.current_hiv_status == POS and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status_with_without_evidence = POS
            elif (self.current_hiv_status == POS and self.rapid_test_done == NO and
                    self.rapid_test_result is None):
                hiv_status_with_without_evidence = UNKNOWN
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == YES and
                    self.rapid_test_result == NEG):
                hiv_status_with_without_evidence = NEG
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status_with_without_evidence = SEROCONVERSION
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == NO and
                    self.rapid_test_result is None):
                hiv_status_with_without_evidence = UNKNOWN
        return hiv_status_with_without_evidence

    def hiv_status_on_or_after_32wk(self, exception_cls=None):
        """Returns the maternal status on or after week 32 gestational age or None."""
        exception_cls = exception_cls or ValidationError
        hiv_status_on_or_after_32wk = None
        if self.week32_test == YES and self.week32_test_date:
            if not self.test_date_is_on_or_after_32wks_gestational_age:
                raise exception_cls(
                    'Test date is not on or after 32 weeks gestational age.')
            elif self.week32_result == POS and self.current_hiv_status == POS:
                hiv_status_on_or_after_32wk = POS
            elif self.week32_result == NEG and self.current_hiv_status == NEG:
                hiv_status_on_or_after_32wk = NEG
        return hiv_status_on_or_after_32wk

    def common_fields(self):
        """Returns a list of field names common to postnatal
        and antenatal enrollment models."""
        return [field.name for field in EnrollmentMixin._meta.fields if field.name not in ['is_eligible']]

    def get_registration_datetime(self):
        return self.report_datetime

    @property
    def subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        abstract = True
