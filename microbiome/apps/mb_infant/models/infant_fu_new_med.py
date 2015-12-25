from django.db import models

from edc_base.model.fields.custom_fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import DRUG_ROUTE
from edc_constants.choices import YES_NO
from edc_visit_tracking.models import CrfInlineModelMixin

from microbiome.apps.mb.choices import MEDICATIONS

from ..managers import InfantInlineModelManager

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantFuNewMed(InfantScheduledVisitModel):

    """ A model completed by the user on the infant's follow up medications. """

    new_medications = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Has the child recieved a NEW course of any of the following medications "
                     "since the last attended scheduled visit",
        help_text="do not report if the same course was recorded at previous visit. "
                  "only report oral and intravenous meds",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant FollowUp: New Medication"
        verbose_name_plural = "Infant FollowUp: New Medication"


class InfantFuNewMedItems(CrfInlineModelMixin, BaseUuidModel):

    """A model completed by the user on the infant's follow up medication items."""

    fk_model_attr = 'infant_fu_med'

    infant_fu_med = models.ForeignKey(InfantFuNewMed)

    medication = models.CharField(
        max_length=100,
        choices=MEDICATIONS,
        verbose_name="Medication",
        blank=True,
        null=True,
    )

    other_medication = OtherCharField()

    date_first_medication = models.DateField(
        verbose_name="Date of first medication use",
    )

    stop_date = models.DateField(
        verbose_name="Date medication was stopped",
        blank=True,
        null=True,
    )

    drug_route = models.CharField(
        max_length=20,
        choices=DRUG_ROUTE,
        verbose_name="Drug route",
    )

    objects = InfantInlineModelManager()

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant FollowUp: New Med Items"
        verbose_name_plural = "Infant FollowUp: New Med Items"
