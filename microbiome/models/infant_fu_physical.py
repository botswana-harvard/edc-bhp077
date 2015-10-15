from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.models import BaseUuidModel

from edc_base.model.fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO

from .infant_fu import InfantFu


class InfantFuPhysical(BaseUuidModel):

    """Infant follow up physical assessment."""

    infant_fu = models.OneToOneField(InfantFu)

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Weight ",
        help_text="Measured in kg.",
    )

    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Height ",
        help_text="",
    )

    head_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="What was the head circumference in centimeters? ",
        help_text="Measured in centimeters, (cm)",
    )

    has_abnormalities = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Abnormal findings ",
        help_text="If 'YES', continue.",
    )

    abnormalities = OtherCharField(
        max_length=100,
        verbose_name="Describe abnormal physical findings",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfuphysical_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = "Infant FollowUp: Physical"
        verbose_name_plural = "Infant FollowUp: Physical"
