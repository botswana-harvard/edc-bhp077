from django.db import models
from django.utils import timezone

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import DRUG_ROUTE
from edc_constants.choices import YES_NO_UNKNOWN

from bhp077.apps.microbiome.choices import MEDICATIONS

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalPostFuMed(MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's Post-partum follow up of medications. """

    CONSENT_MODEL = MaternalConsent

    has_taken_meds = models.CharField(
        max_length=10,
        choices=YES_NO_UNKNOWN,
        verbose_name=("Since the last scheduled visit, has the mother taken any of the following medications?"),
        help_text="",)

    def get_report_datetime(self):
        return self.maternal_visit.get_report_datetime()

    def get_subject_identifier(self):
        return self.maternal_visit.get_subject_identifier()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: Medications"
        verbose_name_plural = "Maternal Postnatal Follow-Up: Medications"


class MaternalPostFuMedItems(BaseUuidModel):

    maternal_post_fu_med = models.OneToOneField(MaternalPostFuMed)

    date_first_medication = models.DateField(
        verbose_name="Date of first medication use",
        default=timezone.now().date()
    )

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

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.maternal_post_fu_med.maternal_visit)

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: Medications"
        verbose_name_plural = "Maternal Postnatal Follow-Up: Medications Items"
