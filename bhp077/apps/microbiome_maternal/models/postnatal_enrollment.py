from django.core.urlresolvers import reverse
from django.db import models

from edc_constants.choices import YES_NO, YES, NO, POS, NEG
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)

from ..maternal_choices import LIVE_STILL_BIRTH, LIVE
from .base_enrollment import BaseEnrollment
from .maternal_consent import MaternalConsent
from .antenatal_enrollment import AntenatalEnrollment


class PostnatalEnrollment(BaseEnrollment):

    CONSENT_MODEL = MaternalConsent

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time of  Postnatal Enrollment",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    postpartum_days = models.IntegerField(
        verbose_name="How many days postpartum?",
        help_text="If more than 3days, not eligible")

    delivery_type = models.CharField(
        verbose_name="Was this a vaginal delivery?",
        choices=YES_NO,
        max_length=3,
        help_text="INELIGIBLE if NO")

    gestation_before_birth = models.IntegerField(
        verbose_name="How many weeks after gestation was the child born?",
        help_text="ineligible if premature or born before 37weeks")

    live_or_still_birth = models.CharField(
        verbose_name="Was this a live or still birth?",
        choices=LIVE_STILL_BIRTH,
        max_length=15,
        help_text='if still birth, not eligible')

    postnatal_enrollemet_eligible = models.NullBooleanField(
        editable=False)

    live_infants = models.IntegerField(
        verbose_name="How many live infants?",
        null=True,
        blank=True)

    def save(self, *args, **kwargs):
        self.postnatal_enrollemet_eligible = self.postnatal_eligible
        super(PostnatalEnrollment, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.report_datetime

    def number_of_weeks_after_tests(self):
        value = self.gestation_before_birth - self.weeks_between(self.date_of_test, self.report_datetime.date())
        return value

    def validate_rapid_test_required_or_not_required(self):
        return self.number_of_weeks_after_tests >= 32

    @property
    def postnatal_eligible(self):
        """Returns true if the participant is eligible."""
        if (self.breastfeed_for_a_year == YES and self.on_tb_treatment == NO and
                self.on_hypertension_treatment == NO and self.is_diabetic == NO and
                self.instudy_for_a_year == YES and self.postpartum_days <= 3 and self.delivery_type == YES and
                self.live_or_still_birth == LIVE and self.gestation_before_birth >= 37):
            if (self.verbal_hiv_status == POS and self.evidence_hiv_status == YES and self.valid_regimen == YES and
                    self.valid_regimen_duration == YES):
                return True
            elif (self.verbal_hiv_status == POS and self.evidence_hiv_status == NO and
                    self.rapid_test_result == POS and self.valid_regimen == YES and self.valid_regimen_duration == YES):
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == NO and self.rapid_test_result == NEG:
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == YES:
                return True
            elif (self.verbal_hiv_status in ['Never tested for HIV', 'Unknown', 'Refused to answer'] and
                    self.rapid_test_result == NEG):
                return True
        return False

    @property
    def antenatal_enrollment(self):
        try:
            return AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return None
        return None

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
