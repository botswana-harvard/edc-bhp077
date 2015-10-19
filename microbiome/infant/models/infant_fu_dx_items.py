from django.db import models
from django.core.urlresolvers import reverse

from edc_constants.choices import YES_NO
from edc_base.model.models import BaseUuidModel

from microbiome.choices import DX_INFANT

from .infant_fu_dx import InfantFuDx


class InfantFuDxItems(BaseUuidModel):

    infant_fu_dx = models.ForeignKey(InfantFuDx)

    fu_dx = models.CharField(
        max_length=150,
        choices=DX_INFANT,
        verbose_name="Diagnosis",
        # null = True,
        help_text="",
    )

    fu_dx_specify = models.CharField(
        max_length=50,
        verbose_name="Diagnosis specification",
        help_text="",
        blank=True,
        null=True,
    )

    health_facility = models.CharField(
        choices=YES_NO,
        max_length=3,
        verbose_name="Seen at health facility for Dx",
        help_text="",
        # null = True,
    )

    was_hospitalized = models.CharField(
        choices=YES_NO,
        max_length=3,
        verbose_name="Hospitalized?",
        help_text="",
        # null = True,
    )

    def __str__(self):
        return str(self.infant_fu_dx.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfudxitems_change', args=(self.id,))

    class Meta:
        app_label = "infant"
        verbose_name = "Infant FollowUp: Dx Items"
        verbose_name_plural = "Infant FollowUp: Dx Items"
