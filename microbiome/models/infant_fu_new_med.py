from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

from edc_base.model.fields.custom_fields import OtherCharField
from edc_constants.choices import YES_NO

from .infant_fu import InfantFu


class InfantFuNewMed(models.Model):

    infant_fu = models.OneToOneField(InfantFu)

    new_medications = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Has the child recieved a NEW course of any of the following medications "
                     "since the last attended scheduled visit",
        help_text="do not report if the same course was recorded at previous visit. "
                  "only report oral and intravenous meds",
    )

    other_medications = OtherCharField(
        max_length=35,
        verbose_name="Other medication that is important to report,in the view of the investigator(either because "
                     "of potential overlapping toxicity with study CTX/placebo or NVP,or for some other "
                     "reason(specify medication)",
        help_text="",
    )

    date_first_medication = models.DateField(
        verbose_name="Date of first medication use",
        default=timezone.now().date()
    )

    def __str__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_infantfunewmed_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = "Infant FollowUp: New Medication"
