from django.db import models
from django.core.urlresolvers import reverse

from edc_base.model.fields import IsDateEstimatedField, OtherCharField
from edc_constants.choices import YES_NO

from ..maternal_choices import PRIOR_PREG_HAART_STATUS
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from microbiome.list.models import PriorArv


class MaternalArvHistory(MaternalScheduledVisitModel):

    """ARV history for infected mothers only"""

    haart_start_date = models.DateField(
        verbose_name="Date of HAART first started",
        help_text="",
    )
    is_date_estimated = IsDateEstimatedField(
        verbose_name=("Is the subject's date of HAART estimated?"),
    )
    preg_on_haart = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Was she still on HAART at the time she became pregnant for this pregnancy? ",
        help_text="",
    )
    haart_changes = models.IntegerField(
        verbose_name="How many times did you change your HAART medicines?",
        help_text="",
    )
    prior_preg = models.CharField(
        max_length=80,
        verbose_name="Prior to this pregnancy the mother has ",
        choices=PRIOR_PREG_HAART_STATUS,
        help_text="",
    )
    prior_arv = models.ManyToManyField(
        PriorArv,
        verbose_name="Please list all of the ARVs that the mother "
        "ever received prior to the current pregnancy:",
        help_text="",
    )
    prior_arv_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternalarvhistory_change', args=(self.id,))

    class Meta:
        app_label = 'maternal'
        verbose_name = "Maternal ARV History"
        verbose_name_plural = "Maternal ARV History"
