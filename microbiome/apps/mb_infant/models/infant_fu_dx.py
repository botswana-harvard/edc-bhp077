from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO
from edc_base.model.models import BaseUuidModel
from edc_visit_tracking.models import CrfInlineModelMixin

from microbiome.apps.mb.choices import DX_INFANT

from ..managers import InfantInlineModelManager

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantFuDx(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's follow up dx. """

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant FollowUp: Dx"
        verbose_name_plural = "Infant FollowUp: Dx"


class InfantFuDxItems(CrfInlineModelMixin, BaseUuidModel):

    fk_model_attr = 'infant_fu_dx'

    infant_fu_dx = models.ForeignKey(InfantFuDx)

    fu_dx = models.CharField(
        verbose_name="Diagnosis",
        max_length=150,
        choices=DX_INFANT)

    fu_dx_specify = models.CharField(
        verbose_name="Diagnosis specification",
        max_length=50,
        blank=True,
        null=True)

    health_facility = models.CharField(
        verbose_name="Seen at health facility for Dx",
        choices=YES_NO,
        max_length=3)

    was_hospitalized = models.CharField(
        verbose_name="Hospitalized?",
        choices=YES_NO,
        max_length=3)

    objects = InfantInlineModelManager()

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant FollowUp: Dx"
