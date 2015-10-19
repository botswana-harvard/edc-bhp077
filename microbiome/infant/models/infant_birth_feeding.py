from django.db import models

from edc_base.model.models import BaseUuidModel

from ..choices import FEEDING_CHOICES

from .infant_birth import InfantBirth
from .infant_visit import InfantVisit


class InfantBirthFeedVaccine(BaseUuidModel):

    """infant feeding"""

    infant_visit = models.ForeignKey(InfantVisit)

    infant_birth = models.ForeignKey(InfantBirth)

    feeding_after_delivery = models.CharField(
        max_length=50,
        choices=FEEDING_CHOICES,
        verbose_name="How was the infant being fed immediately after delivery? ",
        help_text=" ...before discharge from maternity",
    )

    vaccination = models.CharField(
        verbose_name="Since delivery, did the child receive any of the following vaccinations",
        max_length=100,
        help_text="Select all that apply",
    )

    comments = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = "Infant Birth Feeding & Vaccination"
