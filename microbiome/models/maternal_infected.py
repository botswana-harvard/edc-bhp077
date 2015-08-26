from django.db import models
from django.core.urlresolvers import reverse

from .base_mother import BaseMother
from edc_constants.choices import YES_NO, YES_NO_NA

class MaternalInfected(BaseMother):
    
    prior_health_haart = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Before this pregnancy, was the mother on HAART for her own health",
        help_text="For her own health and not just PMTCT for an earlier pregnancy or breastfeeding.",
        )
    prev_pregnancy_arv = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name="Was the mother on any ARVs during previous pregnancies (or immediately following delivery) for PMTCT purposes (and not for her own health)? ",
        help_text="not including this pregnancy", )
    
    def get_absolute_url(self):
        return reverse('admin:microbiome_maternalinfected_change', args=(self.id,))
    
    class Meta:
        app_label = 'microbiome'
        verbose_name = 'Maternal Infected'
        verbose_name_plural = 'Maternal Infected'
