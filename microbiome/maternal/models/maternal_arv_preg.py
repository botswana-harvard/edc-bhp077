from django.db import models

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from edc_constants.choices import YES_NO


class MaternalArvPreg(MaternalScheduledVisitModel):

    """ This form is for all HIV positive mothers who are pregnant (whom we hope to enroll their infant)
     and/or for mothers who have just delivered """

    took_arv = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother receive any ARVs during this pregnancy?",
        help_text="(NOT including single -dose NVP in labour)")

    is_interrupt = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name=("Was there an interruption in the ARVs received during pregnancy "
                      "through delivery of >/=3days?"),
        help_text="")

    interrupt = models.CharField(
        verbose_name="Please give reason for interruption",
        max_length=50,
        help_text="",
        default='N/A')

    interrupt_other = models.TextField(
        max_length=250,
        verbose_name="Other, specify ",
        blank=True,
        null=True)

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments on pregnancy regimen: ",
        blank=True,
        null=True)

    class Meta:
        app_label = "microbiome"
        verbose_name = 'Maternal ARV In This Preg: Pregnancy'
        verbose_name_plural = 'Maternal ARV In This Preg: Pregnancy'


class MaternalArv(MaternalScheduledVisitModel):

    """ ARV table to indicate ARV medication taken by mother """

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg)

    arv_code = models.CharField(
        verbose_name="ARV code",
        null=True,
        blank=True,
        max_length=25)

    date_started = models.DateField(
        verbose_name="Date Started",
        null=True,
        blank=True)

    date_stopped = models.DateField(
        verbose_name="Date Stopped",
        null=True,
        blank=True)

    class Meta:
        app_label = 'maternal'
        verbose_name = 'Maternal ARV'
        verbose_name_plural = 'Maternal ARV'
