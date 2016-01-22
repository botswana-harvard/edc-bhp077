from datetime import date

from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import DRUG_ROUTE, YES_NO_UNKNOWN
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfInlineModelMixin

from microbiome.apps.mb.choices import MEDICATIONS

from ..managers import MaternalPostMedItemsManager

from .maternal_crf_model import MaternalCrfModel


class MaternalPostFuMed(MaternalCrfModel):

    """ A model completed by the user on the mother's Post-partum follow up of medications. """

    has_taken_meds = models.CharField(
        verbose_name=(
            "Since the last scheduled visit, has the mother taken any of the following medications?"),
        max_length=10,
        choices=YES_NO_UNKNOWN)

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Maternal Postnatal: Med'


class MaternalPostFuMedItems(CrfInlineModelMixin, SyncModelMixin, BaseUuidModel):

    fk_model_attr = 'maternal_post_fu_med'

    maternal_post_fu_med = models.OneToOneField(MaternalPostFuMed)

    date_first_medication = models.DateField(
        verbose_name="Date of first medication use",)

    medication = models.CharField(
        max_length=100,
        choices=MEDICATIONS,
        verbose_name="Medication",
    )

    drug_route = models.CharField(
        max_length=20,
        choices=DRUG_ROUTE,
        verbose_name="Drug route",
    )

    date_stoped = models.DateField(
        verbose_name="Date medication was stopped",
        blank=True,
        null=True,
    )

    objects = MaternalPostMedItemsManager()

    history = AuditTrail()

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Postnatal: Med Item"
