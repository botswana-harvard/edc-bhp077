from django.db import models

from edc_constants.constants import NO, YES, POS, NEG, NOT_APPLICABLE
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)

from .enrollment_mixin import EnrollmentMixin
from .maternal_consent import MaternalConsent


class AntenatalEnrollment(EnrollmentMixin):

    CONSENT_MODEL = MaternalConsent

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time of  Antenatal Enrollment",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    weeks_of_gestation = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        help_text=" (weeks of gestation). Eligible if >=36 weeks", )

    antenatal_eligible = models.NullBooleanField(
        editable=False)

    @property
    def number_of_weeks_after_tests(self):
        value = self.weeks_of_gestation - self.weeks_between(self.date_of_test, self.report_datetime.date())
        return value

    def validate_rapid_test_required_or_not_required(self):
        return self.number_of_weeks_after_tests >= 32

    def save(self, *args, **kwargs):
        self.antenatal_eligible = self.eligible_for_postnatal
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.report_datetime

    @property
    def eligible_for_postnatal(self):
        """return true if a mother is eligible for postnatalenrollment."""
        if self.weeks_of_gestation >= 36 and self.is_diabetic == NO and self.on_tb_treatment == NO and self.on_hypertension_treatment == NO and self.breastfeed_for_a_year == YES and self.instudy_for_a_year == YES:
            if self.week32_test == YES and self.week32_result == POS and self.evidence_hiv_status == YES:
                return True
            if self.week32_test == YES and self.week32_result == NEG and self.evidence_hiv_status == YES:
                return True
            if (self.week32_test == NO and self.process_rapid_test == YES and self.evidence_hiv_status == NO and not self.week32_result):
                return True
            if self.week32_test == NO and self.process_rapid_test == YES and self.evidence_hiv_status == NOT_APPLICABLE and not self.week32_result:
                return True
            if self.verbal_hiv_status == POS and self.evidence_hiv_status == YES and self.valid_regimen == YES and self.valid_regimen_duration == YES:
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == YES:
                return True
            elif self.evidence_hiv_status == NO and self.rapid_test_result != POS and self.process_rapid_test == YES:
                return True
        return False

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
