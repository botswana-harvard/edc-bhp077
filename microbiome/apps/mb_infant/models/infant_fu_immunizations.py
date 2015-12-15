from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO_UNKNOWN
from edc_base.model.models import BaseUuidModel

from microbiome.apps.mb.choices import REASONS_VACCINES_MISSED

from ..choices import IMMUNIZATIONS, INFANT_AGE_VACCINE_GIVEN
from ..managers import InfantInlineModelManager

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantFuImmunizations(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's follow up immunizations. """

    vaccines_received = models.CharField(
        max_length=25,
        choices=YES_NO_UNKNOWN,
        verbose_name="Did this infant receive any vaccinations since the last visit",
        help_text="")

    vaccines_missed = models.CharField(
        max_length=25,
        choices=YES_NO_UNKNOWN,
        verbose_name="Is the child missing any vaccinations?",
        help_text="")

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.infant_visit)

    class Meta:
        app_label = 'mb_infant'
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

    objects = InfantInlineModelManager()

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.infant_fu_immunizations)

    def get_visit(self):
        return self.infant_fu_immunizations.infant_visit

    def get_report_datetime(self):
        return self.get_visit().get_report_datetime()

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    class Meta:
        app_label = 'mb_infant'
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

    objects = InfantInlineModelManager()

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.infant_fu_immunizations)

    def natural_key(self):
        return self.get_visit().natural_key()

    def get_visit(self):
        return self.infant_fu_immunizations.infant_visit

    def get_report_datetime(self):
        return self.get_visit().get_report_datetime()

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = 'Missed Vaccines'
        verbose_name_plural = 'Missed Vaccines'
