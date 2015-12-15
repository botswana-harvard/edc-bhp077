from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_base.model.fields.custom_fields import IsDateEstimatedField
from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO_NA, YES_NO

from .maternal_consent import MaternalConsent
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from bhp077.apps.microbiome_maternal.maternal_choices import KNOW_HIV_STATUS


class MaternalClinicalHistory(MaternalScheduledVisitModel):

    CONSENT_MODEL = MaternalConsent

    """ A model completed by the user on Clinical History for infected mothers only. """

    prev_preg_azt = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name="Did she ever receive AZT monotherapy in a previous pregnancy?  ")

    prev_sdnvp_labour = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name="Did she ever receive single-dose NVP in labour during a previous pregnancy?")

    prev_preg_haart = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name=("Did she ever receive triple antiretrovirals during a prior pregnancy?"))

    lowest_cd4_known = models.CharField(
        max_length=4,
        choices=YES_NO,
        verbose_name="Is the mother's lowest CD4 known?"
    )

    cd4_count = models.IntegerField(
        verbose_name=("What was the mother's lowest known (nadir) CD4 cell count(cells/mm3)"
                      " at any time in the past?"),
        validators=[MinValueValidator(0), MaxValueValidator(3000), ],
        null=True,
        blank=True,
    )

    cd4_date = models.DateField(
        verbose_name="Year/Month of CD4 test ",
        help_text="Format is YYYY-MM-DD. Use 01 for Day",
        blank=True,
        null=True)

    is_date_estimated = IsDateEstimatedField(
        verbose_name=("Is the subject's date of CD4 test estimated?"),
        blank=True,
        null=True
    )

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments",
        blank=True,
        null=True)

    prior_health_haart = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Before this pregnancy, was the mother on HAART for her own health",
        help_text=("For her own health and not just PMTCT for an earlier pregnancy or "
                   "breastfeeding.",))
    prev_pregnancy_arv = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name="Was the mother on any ARVs during previous pregnancies (or immediately following delivery) "
                     "for PMTCT purposes (and not for her own health)? ",
        help_text="not including this pregnancy", )

    know_hiv_status = models.CharField(
        max_length=50,
        verbose_name="How many people know that you are HIV infected?",
        choices=KNOW_HIV_STATUS)

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal use of ARVs in Prior Pregnancy'
        verbose_name_plural = 'Maternal use of ARVs in Prior Pregnancy'
