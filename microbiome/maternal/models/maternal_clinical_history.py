from django.db import models
from django.core.urlresolvers import reverse


from edc_base.model.fields.custom_fields import IsDateEstimatedField
from maternal.models.maternal_scheduled_visit_model import MaternalScheduledVisitModel
from edc_constants.choices import YES_NO


class MaternalClinicalHistory(MaternalScheduledVisitModel):

    """Clinical History for infected mothers only."""

    prev_preg_azt = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Did she ever receive AZT monotherapy in a previous pregnancy?  ",
        help_text="")

    prev_sdnvp_labour = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Did she ever receive single-dose NVP in labour during a previous pregnancy?",
        help_text="")

    prev_preg_haart = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=("Did she ever receive HAART (for PMTCT purposes only) during a "
                      "previous pregnancy? "),
        help_text="")

    cd4_count = models.IntegerField(
        verbose_name=("What was the mother's lowest known (nadir) CD4 cell count(cells/mm3)"
                      " at any time in the past?"),
        help_text="")

    cd4_date = models.DateField(
        verbose_name="Year/Month of CD4 test ",
        help_text="Format is YYYY-MM-DD. Use 01 for Day",
        blank=True,
        null=True)

    is_date_estimated = IsDateEstimatedField(
        verbose_name=("Is the subject's date of CD4 test estimated?"))

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments",
        blank=True,
        null=True)

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternalclinicalhistory_change', args=(self.id,))

    class Meta:
        app_label = "microbiome"
        verbose_name = 'Maternal Clinical History'
        verbose_name_plural = 'Maternal Clinical History'
