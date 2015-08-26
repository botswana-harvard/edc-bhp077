from django.db import models
from django.core.urlresolvers import reverse

from ..choices import RECRUIT_SOURCE, RECRUIT_CLINIC
from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel

class BaseMother(BaseUuidModel):

    """Base Model for infected and uninfected mothers
    """

    recruit_source = models.CharField(
        max_length=75,
        choices=RECRUIT_SOURCE,
        verbose_name="The mother first learned about the Microbiome study from ",
        help_text="",
        )
    recruit_source_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
        )
    recruitment_clinic = models.CharField(
        max_length=100,
        verbose_name="The mother was recruited from",
        choices=RECRUIT_CLINIC,
        )
    recruitment_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other specify...",
        blank=True,
        null=True,
        )
    prev_pregnancies = models.IntegerField(
        verbose_name="Not including this pregnancy, how many previous pregnancies for this participant?",
        help_text="",
        )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Mother's weight? ",
        help_text="Measured in Kilograms (kg)",
        )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Mother's height? ",
        help_text="Measured in Centimeters (cm)",
        )
    bp = models.CharField(
        max_length=7,
        verbose_name="Mother's blood pressure?",
        help_text="in mm/hg E.G. 120/80 ",
        )

    class Meta:
        abstract = True
