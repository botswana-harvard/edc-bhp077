from django.core.urlresolvers import reverse
from django.db import models

from .base_enrollment import BaseEnrollment
from ..maternal_choices import LIVE_STILL_BIRTH
from edc_constants.choices import YES_NO
from .maternal_consent import MaternalConsent
from .antenatal_enrollment import AntenatalEnrollment


class PostnatalEnrollment(BaseEnrollment):

    CONSENT_MODEL = MaternalConsent

    def save_postnatal_enrollment(self):
        """Confirms if antenatal enrollment exists"""
        try:
            ante_natal = AntenatalEnrollment.objects.get(
                CONSENT_MODEL__subject_identifier=self.CONSENT_MODEL.subject_identifier)
            if ante_natal:
                data = {self.citizen: 'citizen',
                        self.is_diabetic: 'is_diabetic',
                        self.on_tb_treatment: 'on_tb_treatment',
                        self.breastfeed_for_a_year: 'breastfeed_for_a_year',
                        self.instudy_for_a_year: 'instudy_for_a_year',
                        self.verbal_hiv_status: 'verbal_hiv_status',
                        self.evidence_hiv_status: 'evidence_hiv_status',
                        self.valid_regimen: 'valid_regimen',
                        self.process_rapid_test: 'process_rapid_test',
                        self.date_of_rapid_test: 'date_of_rapid_test',
                        self.rapid_test_result: 'rapid_test_result'}
        except AntenatalEnrollment.DoesNotExist:
            pass

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

    live_infants = models.IntegerField(
        verbose_name="How many live infants?",
        null=True,
        blank=True)

    def get_absolute_url(self):
        return reverse('admin:microbiome_postnatalenrollment_change', args=(self.id,))

    class Meta:
        app_label = 'maternal'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
