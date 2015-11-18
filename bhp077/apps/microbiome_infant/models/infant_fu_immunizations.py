from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.fields import OtherCharField
from edc_base.model.validators.date import date_not_future
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO_UNKNOWN

from .infant_fu import InfantFu
from .infant_scheduled_visit_model import InfantScheduledVisitModel
from bhp077.apps.microbiome.choices import REASONS_VACCINES_MISSED


class InfantFuImmunizations(InfantScheduledVisitModel):

    infant_fu = models.OneToOneField(InfantFu)

    vaccines_received = models.CharField(
        max_length=25,
        choices=YES_NO_UNKNOWN,
        verbose_name="Did this infant receive any vaccinations since the last visit",
        help_text="")

    vaccines_missed = models.CharField(
        max_length=25,
        choices=YES_NO_UNKNOWN,
        verbose_name="Is the child missing any vacations?",
        help_text="")

    history = AuditTrail()

    def __str__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_infantfuimmunization_change', args=(self.id,))

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant FollowUp: Immunizations"
        verbose_name_plural = "Infant FollowUp: Immunizations"


class VaccinesReceived(InfantScheduledVisitModel):

    """ALL possible vaccines given to infant"""

    infant_fu_immunizations = models.ForeignKey(InfantFuImmunizations)

    received_vaccine_name = models.CharField(
        verbose_name="Received vaccine name",
        null=True,
        blank=True,
        max_length=25)

    date_given = models.DateField(
        verbose_name="Date Given",
        null=True,
        blank=True)

    class Meta:
        app_label = 'microbiome_infant'
        verbose_name = 'Received Vaccines'
        verbose_name_plural = 'Received Vaccines'


class VaccinesMissed(InfantScheduledVisitModel):

    """ALL vaccines missed by infant"""

    infant_fu_immunizations = models.ForeignKey(InfantFuImmunizations)

    missed_vaccine_name = models.CharField(
        verbose_name="Missed vaccine name",
        null=True,
        blank=True,
        max_length=25)

    reason_missed = models.DateField(
        verbose_name="Reasons infant missed vaccines",
        choices=REASONS_VACCINES_MISSED,
        null=True,
        blank=True)

    reason_missed_other = OtherCharField()

    class Meta:
        app_label = 'microbiome_infant'
        verbose_name = 'Missed Vaccines'
        verbose_name_plural = 'Missed Vaccines'
