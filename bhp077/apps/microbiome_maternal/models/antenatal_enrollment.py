from django.core.urlresolvers import reverse
from django.db import models

from edc_constants.constants import NO, YES, POS, NEG

from .base_enrollment import BaseEnrollment
from .maternal_consent import MaternalConsent


class AntenatalEnrollment(BaseEnrollment):

    CONSENT_MODEL = MaternalConsent

    weeks_of_gestation = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        help_text=" (weeks of gestation). Eligible if >=32 weeks", )

    antenatal_eligible = models.NullBooleanField(
        editable=False)

    def save(self, *args, **kwargs):
        self.antenatal_eligible = self.eligible_for_postnatal
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    @property
    def eligible_for_postnatal(self):
        """return true if a mother is eligible for postnatalenrollment."""
        if self.weeks_of_gestation >= 32 and self.is_diabetic == NO and self.on_tb_treatment == NO and self.on_hypertension_treatment == NO and self.breastfeed_for_a_year == YES and self.instudy_for_a_year:
            if self.verbal_hiv_status == POS and self.evidence_hiv_status == YES and self.valid_regimen == YES and self.valid_regimen_duration == YES:
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == YES:
                return True
            elif self.evidence_hiv_status == NO and self.rapid_test_result == POS and self.weeks_of_gestation == 32:
                return True
            elif self.evidence_hiv_status == NO and self.rapid_test_result != POS and self.process_rapid_test == YES:
                return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_antenatalenrollment_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
