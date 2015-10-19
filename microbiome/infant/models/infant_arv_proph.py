from django.db import models
from django.core.urlresolvers import reverse

from edc_constants.choices import YES_NO
from microbiome.choices import ARV_STATUS_WITH_NEVER
# from edc.subject.haart.choices import ARV_STATUS_WITH_NEVER


class InfantArvProph(models.Model):

    prophylatic_nvp = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was the baby supposed to be taking taking prophylactic antiretroviral medication for "
                     "any period since the last attended scheduled visit?",
    )

    arv_status = models.CharField(
        max_length=25,
        verbose_name="What is the status of the participant's ARV prophylaxis at this visit or since the last visit? ",
        choices=ARV_STATUS_WITH_NEVER,
        help_text="referring to prophylaxis other than single dose NVP",
        default='N/A',
    )

    def __str__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantarvproph_change', args=(self.id,))

    class Meta:
        app_label = "infant"
        verbose_name = 'Infant NVP or AZT Proph'
