from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN


class MaternalArvPreg(BaseUuidModel):

    """ Maternal arv for current pregnancy. """

    # if yes, complete MaternalArvPregHistory
    took_arv = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother receive any ARVs during this pregnancy?",
        help_text="(NOT including single -dose NVP in labour)",
    )

    sd_nvp = models.CharField(
        max_length=10,
        choices=YES_NO_UNKNOWN,
        verbose_name="Was single-dose NVP received by the mother during labour(or false labour)? ",
        help_text="",
    )

    # if yes, complete MaternalArvPostPart
    start_pp = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother START any antiretroviral drugs during the immediate "
        "postpartum period (before discharge from maternity)?",
        help_text="",
    )

    class Meta:
        app_label = "microbiome"


class MaternalArvPregHistory(BaseUuidModel):

    """ Maternal arv for current pregnancy (transactions). """

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg)

    is_interrupt = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was there an interruption in the ARVs received during pregnancy through delivery of >/=3days?",
        help_text="",
    )

    interrupt = models.CharField(
        verbose_name="Please give reason for interruption",
        max_length=50,
        help_text="",
        default='N/A',
    )

    interrupt_other = models.TextField(
        max_length=250,
        verbose_name="Other, specify ",
        blank=True,
        null=True,
    )

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments on pregnancy regimens: ",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = 'Maternal ARV In This Preg: Pregnancy'


class MaternalArvPPHistory(BaseUuidModel):

    """ Maternal arv for post-partum (transactions). """

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg)

    comment = models.CharField(
        max_length=35,
        verbose_name="Comments postpartum regimens: ",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = 'Maternal ARV In This Preg: PostPart'


class MaternalArv():

    """ Maternal arv history (current and post-partum). """

    maternal_arv_preg_history = models.ForeignKey(
        MaternalArvPregHistory,
        null=True,
        blank=True,
    )

    maternal_arv_pp_history = models.ForeignKey(
        MaternalArvPPHistory,
        null=True,
        blank=True,
    )

    transaction_flag = models.CharField(
        verbose_name="Transaction flag",
        max_length=15,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "microbiome"
        verbose_name = 'Maternal ARV'
