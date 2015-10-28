from django.db import models

from microbiome.choices import DRUG_RELATIONSHIP

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantDeath (InfantScheduledVisitModel):

    death_reason_hospitalized_other = models.TextField(
        verbose_name="if other illness or pathogen specify or non infectious reason, please specify below:",
        max_length=250,
        blank=True,
        null=True,
    )

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

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Death"
