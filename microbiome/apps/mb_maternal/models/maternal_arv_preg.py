from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO, ARV_DRUG_LIST
from edc_constants.constants import NOT_APPLICABLE
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfInlineModelMixin

from microbiome.apps.mb.choices import ARV_INTERRUPTION_REASON

from ..managers import MaternalArvManager

from .maternal_crf_model import MaternalCrfModel


class MaternalArvPreg(MaternalCrfModel):

    """ This model is for all HIV positive mothers who are pregnant (whom we hope to enroll their infant)
     and/or for mothers who have just delivered """

    took_arv = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Did the mother receive any ARVs during this pregnancy?",
        help_text="(NOT including single -dose NVP in labour)")

    is_interrupt = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Was there an interruption in the ARVs received during pregnancy through delivery of >/=3days?",
    )

    interrupt = models.CharField(
        verbose_name="Please give reason for interruption",
        max_length=50,
        choices=ARV_INTERRUPTION_REASON,
        default=NOT_APPLICABLE)

    interrupt_other = models.TextField(
        max_length=250,
        verbose_name="Other, specify ",
        blank=True,
        null=True)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Maternal ARV In This Preg'
        verbose_name_plural = 'Maternal ARV In This Preg'


class MaternalArv(CrfInlineModelMixin, SyncModelMixin, BaseUuidModel):

    """ ARV table to indicate ARV medication taken by mother """

    fk_model_attr = 'maternal_arv_preg'

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg)

    arv_code = models.CharField(
        verbose_name="ARV code",
        max_length=35,
        choices=ARV_DRUG_LIST,)

    start_date = models.DateField(
        verbose_name="Date Started")

    stop_date = models.DateField(
        verbose_name="Date Stopped",
        null=True,
        blank=True)

    objects = MaternalArvManager()

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Maternal ARV'
        verbose_name_plural = 'Maternal ARV'
