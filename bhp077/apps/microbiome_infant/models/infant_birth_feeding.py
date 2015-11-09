from django.core.urlresolvers import reverse
from django.db import models

from bhp077.apps.microbiome.choices import FEEDING_CHOICES
from bhp077.apps.microbiome_list.models import InfantVaccines

from .infant_birth import InfantBirth
from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantBirthFeedVaccine(InfantScheduledVisitModel):

    """infant feeding & vaccination/ immunization"""

    infant_birth = models.ForeignKey(InfantBirth)

    feeding_after_delivery = models.CharField(
        max_length=50,
        choices=FEEDING_CHOICES,
        verbose_name="How was the infant being fed immediately after delivery? ",
        help_text=" ...before discharge from maternity")

    vaccination = models.ManyToManyField(
        InfantVaccines,
        verbose_name="Since delivery, did the child receive any of the following vaccinations",
        max_length=100,
        help_text="Select all that apply")

    comments = models.TextField(
        max_length=250,
        verbose_name="Comment if any additional pertinent information: ",
        blank=True,
        null=True)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infant_infantbirthfeedvaccine_change', args=(self.id,))

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Birth Feeding & Vaccination"
        verbose_name_plural = "Infant Birth Feeding & Vaccination"
