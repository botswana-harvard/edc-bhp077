from django.db import models
from django.core.urlresolvers import reverse

from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO
from edc_base.model.models import BaseUuidModel

from .infant_scheduled_visit_model import InfantScheduledVisitModel
from bhp077.apps.microbiome.choices import DX_INFANT


class InfantFuDx(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's follow up dx. """

    def __str__(self):
        return str(self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_infantfudx_change', args=(self.id,))

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

    objects = models.Manager()

    history = AuditTrail()

    def __str__(self):
        return str(self.infant_fu_dx.infant_visit)

    def get_visit(self):
        return self.infant_fu_dx.get_visit()

    def get_report_datetime(self):
        return self.infant_fu_dx.get_report_datetime()

    def get_subject_identifier(self):
        return self.infant_fu_dx.get_subject_identifier()

    def __unicode__(self):
        return unicode(self.get_visit())

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant FollowUp: Dx Items"
        verbose_name_plural = "Infant FollowUp: Dx Items"
