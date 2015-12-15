from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO
from edc_base.model.models import BaseUuidModel

from .infant_scheduled_visit_model import InfantScheduledVisitModel
from ..managers import InfantInlineModelManager

from bhp077.apps.microbiome.choices import DX_INFANT


class InfantFuDx(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's follow up dx. """

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant FollowUp: Dx"
        verbose_name_plural = "Infant FollowUp: Dx"


class InfantFuDxItems(BaseUuidModel):

    infant_fu_dx = models.ForeignKey(InfantFuDx)

    fu_dx = models.CharField(
        max_length=150,
        choices=DX_INFANT,
        verbose_name="Diagnosis",
        help_text="")

    fu_dx_specify = models.CharField(
        max_length=50,
        verbose_name="Diagnosis specification",
        help_text="",
        blank=True,
        null=True)

    health_facility = models.CharField(
        choices=YES_NO,
        max_length=3,
        verbose_name="Seen at health facility for Dx",
        help_text="")

    was_hospitalized = models.CharField(
        choices=YES_NO,
        max_length=3,
        verbose_name="Hospitalized?",
        help_text="",)

    objects = InfantInlineModelManager()

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.infant_fu_dx.infant_visit)

    def get_visit(self):
        return self.infant_fu_dx.get_visit()

    def get_report_datetime(self):
        return self.infant_fu_dx.get_report_datetime()

    def get_subject_identifier(self):
        return self.infant_fu_dx.get_subject_identifier()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant FollowUp: Dx Items"
        verbose_name_plural = "Infant FollowUp: Dx Items"
