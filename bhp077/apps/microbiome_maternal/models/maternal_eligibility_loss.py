from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel

from .maternal_eligibility import MaternalEligibility
from django.utils import timezone


class MaternalEligibilityLoss(BaseUuidModel):
    """ A model triggered and completed by system when a mother is in-eligible. """

    maternal_eligibility = models.OneToOneField(MaternalEligibility, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=timezone.now,
        help_text='Date and time of report.')

    reason_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Gets reasons from Maternal Eligibility.ineligibility')

    objects = models.Manager()

    history = AuditTrail()

    def ineligibility(self):
        return self.reason_ineligible or []
    reason_ineligible.allow_tags = True

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Eligibility Loss'
        verbose_name_plural = 'Maternal Eligibility Loss'
