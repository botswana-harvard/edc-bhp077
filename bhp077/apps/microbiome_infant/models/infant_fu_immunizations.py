from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.fields import OtherCharField
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO_UNKNOWN
from edc_base.model.models import BaseUuidModel

from .infant_fu import InfantFu
from .infant_scheduled_visit_model import InfantScheduledVisitModel
from bhp077.apps.microbiome.choices import REASONS_VACCINES_MISSED
from ..infant_choices import IMMUNIZATIONS, INFANT_AGE_VACCINE_GIVEN


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


class VaccinesReceived(BaseUuidModel):

    """ALL possible vaccines given to infant"""

    infant_fu_immunizations = models.ForeignKey(InfantFuImmunizations)

    received_vaccine_name = models.CharField(
        verbose_name="Received vaccine name",
        null=True,
        choices=IMMUNIZATIONS,
        blank=True,
        max_length=100)

    date_given = models.DateField(
        verbose_name="Date Given",
        null=True,
        blank=True)

    infant_age = models.CharField(
        verbose_name="Infant age when vaccine given",
        choices=INFANT_AGE_VACCINE_GIVEN,
        null=True,
        blank=True,
        max_length=35)

    def get_visit(self):
        return self.infant_fu_immunizations.infant_visit

    def __unicode__(self):
        return "%s" % (self.infant_fu_immunizations)

    def get_report_datetime(self):
        return self.get_visit().get_report_datetime()

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_vaccinesreceived_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_infant'
        verbose_name = 'Received Vaccines'
        verbose_name_plural = 'Received Vaccines'


class VaccinesMissed(BaseUuidModel):

    """ALL vaccines missed by infant"""

    infant_fu_immunizations = models.ForeignKey(InfantFuImmunizations)

    missed_vaccine_name = models.CharField(
        verbose_name="Missed vaccine name",
        choices=IMMUNIZATIONS,
        null=True,
        blank=True,
        max_length=100)

    reason_missed = models.CharField(
        verbose_name="Reasons infant missed vaccines",
        choices=REASONS_VACCINES_MISSED,
        max_length=100,
        null=True,
        blank=True)

    reason_missed_other = OtherCharField()

    def get_visit(self):
        return self.infant_fu_immunizations.infant_visit

    def __unicode__(self):
        return "%s" % (self.infant_fu_immunizations)

    def get_report_datetime(self):
        return self.get_visit().get_report_datetime()

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_vaccinesmissed_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_infant'
        verbose_name = 'Missed Vaccines'
        verbose_name_plural = 'Missed Vaccines'
