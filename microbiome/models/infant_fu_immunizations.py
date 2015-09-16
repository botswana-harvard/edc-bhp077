from django.db import models
from django.core.urlresolvers import reverse

from edc_constants.choices import YES_NO
from edc_base.model.models import BaseUuidModel

from ..choices import REASON_NOT_RECEIVED_VACCINATION

from .infant_fu import InfantFu


class InfantFuImmunizations(BaseUuidModel):

    infant_fu = models.OneToOneField(InfantFu)

    vaccines_received = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Since the last attended scheduled visit,did the child recieve any of the following vaccinations",
        help_text="",
    )

    vaccination = models.CharField(
        verbose_name="Vaccines received",
        max_length=15,
        help_text="Select all the vaccines that were received",
    )

    reason_not_received = models.CharField(
        verbose_name="Reason not received",
        max_length=50,
        choices=REASON_NOT_RECEIVED_VACCINATION,
        help_text="",
    )

    comments = models.TextField(
        max_length=500,
        verbose_name="Comment",
        blank=True,
        null=True,
    )

    def __str__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfumed_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = "Infant FollowUp: Medication"
