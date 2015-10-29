from django.core.urlresolvers import reverse
from datetime import datetime

from django.db import models

from edc_base.model.models import BaseUuidModel

from .maternal_eligibility import MaternalEligibility


class MaternalEligibilityLoss(BaseUuidModel):
    """Triggered and completed by system when a mother is in-eligible"""

    maternal_eligibility = models.OneToOneField(MaternalEligibility, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=datetime.today(),
        help_text='Date and time of report.')

    reason_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Gets reasons from Maternal Eligibility.ineligibility')

    def ineligibility(self):
        return self.reason_ineligible or []
    reason_ineligible.allow_tags = True

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternaleligibilityloss_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Eligibility Loss'
        verbose_name_plural = 'Maternal Eligibility Loss'
