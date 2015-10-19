from django.core.urlresolvers import reverse
from django.db import models

from maternal.models.base_enrollment import BaseEnrollment
from maternal.models.maternal_consent import MaternalConsent


class AntenatalEnrollment(BaseEnrollment):

    CONSENT_MODEL = MaternalConsent

    weeks_of_gestation = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        null=True,
        blank=True,
        help_text=" (weeks of gestation). If >=32 weeks do rapid test", )

    def get_absolute_url(self):
        return reverse('admin:microbiome_antenatalenrollment_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
