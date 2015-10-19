from django.db import models

from edc_base.model.models import BaseUuidModel

from microbiome.choices import (INFO_PROVIDER, INFANT_VISIT_STUDY_STATUS, ALIVE_DEAD_UNKNOWN)


class InfantVisit(BaseUuidModel):

    information_provider = models.CharField(
        verbose_name="Please indicate who provided most of the information for this child's visit",
        choices=INFO_PROVIDER,
        max_length=20,
        help_text="",
    )

    information_provider_other = models.CharField(
        verbose_name="if information provider is Other, please specify",
        max_length=20,
        help_text="",
        blank=True,
        null=True,
    )

    study_status = models.CharField(
        verbose_name="What is the participant's current study status",
        max_length=50,
        choices=INFANT_VISIT_STUDY_STATUS,
    )

    survival_status = models.CharField(
        max_length=10,
        verbose_name="Survival status",
        choices=ALIVE_DEAD_UNKNOWN,
        null=True,
        blank=False
    )

    date_last_alive = models.DateField(
        verbose_name="Date last known alive",
        help_text="",
        null=True,
        blank=True
    )

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Visit"
