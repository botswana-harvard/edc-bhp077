from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.fields import OtherCharField
from maternal.models.maternal_scheduled_visit_model import MaternalScheduledVisitModel
from edc_constants.choices import YES_NO

from microbiome.list import ChronicConditions


class MaternalMedicalHistory(MaternalScheduledVisitModel):

    """Medical History for all mothers"""

    has_chronic_cond = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=("Does the mother have any significant chronic condition(s) that were"
                      " diagnosed prior to the current pregnancy and that remain ongoing?"),)
    chronic_cond = models.ManyToManyField(
        ChronicConditions,
        verbose_name="Chronic Diagnosis. Tick all that apply",
        help_text="")
    chronic_cond_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True)
    who_diagnosis = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO,
        verbose_name=("Prior to the current pregnancy, was the participant ever diagnosed with"
                      " a WHO Stage III or IV illness?"),
        help_text="Please use the WHO Staging Guidelines. ONLY for HIV infected mothers")

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternalmedicalhistory_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Medical History"
        verbose_name_plural = "Maternal Medical History"
