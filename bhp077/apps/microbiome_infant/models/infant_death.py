from django.db import models

from bhp077.apps.microbiome.choices import DRUG_RELATIONSHIP

from edc_base.audit_trail import AuditTrail

from edc.subject.adverse_event.models import BaseDeathReport

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantDeath (InfantScheduledVisitModel, BaseDeathReport):

    """ A model completed by the user after an infant's death. """

    study_drug_relate = models.CharField(
        verbose_name="Relationship between the participant death and study drug (CTX vs Placebo)",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    infant_nvp_relate = models.CharField(
        verbose_name="Relationship between the participant death and infant extended nevirapine prophylaxis ",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    haart_relate = models.CharField(
        verbose_name="Relationship between the participant death and HAART",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    trad_med_relate = models.CharField(
        verbose_name="Relationship between the participant death and traditional medicine use",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    objects = models.Manager()

    history = AuditTrail()

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Death"
