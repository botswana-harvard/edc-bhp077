from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

from edc.subject.adverse_event.choices import GRADING_SCALE
from edc.subject.code_lists.models import WcsDxAdult
from edc_base.audit_trail import AuditTrail
from edc_base.model.fields.custom_fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import DRUG_ROUTE
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN

from bhp077.apps.microbiome.choices import MEDICATIONS
from bhp077.apps.microbiome_list.models import ChronicConditions

from ..managers import MaternalPostFuDxTManager
from ..maternal_choices import DX
from .maternal_consent import MaternalConsent
from .maternal_post_fu import MaternalPostFu
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class MaternalPostFuMed(MaternalScheduledVisitModel):

    """ Post-partum follow up of medications. """

    maternal_post_fu = models.OneToOneField(MaternalPostFu)

    has_taken_meds = models.CharField(
        max_length=3,
        choices=YES_NO_UNKNOWN,
        verbose_name=("Since the last scheduled visit, has the mother taken any of the following medications?"),
        help_text="",)

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternalpostfumed_change', args=(self.id,))

    def get_report_datetime(self):
        return self.maternal_post_fu.get_report_datetime()

    def get_subject_identifier(self):
        return self.maternal_post_fu.get_subject_identifier()

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: Medications"
        verbose_name_plural = "Maternal Postnatal Follow-Up: Medications"


class MaternalPostFuMedItems(BaseUuidModel):

    maternal_post_fu = models.OneToOneField(MaternalPostFuMed)

    date_first_medication = models.DateField(
        verbose_name="Date of first medication use",
        default=timezone.now().date()
    )

    medication = models.CharField(
        max_length=100,
        choices=MEDICATIONS,
        verbose_name="Medication",
        blank=True,
        null=True,
    )

    drug_route = models.CharField(
        max_length=20,
        choices=DRUG_ROUTE,
        verbose_name="Drug route",
        blank=True,
        null=True,
    )

    date_stoped = models.DateField(
        verbose_name="Date medication was stopped",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.maternal_post_fu.maternal_visit)

    def get_absolute_url(self):
        return reverse('admin:microbiome_matrenal_maternalpostfumeditems_change', args=(self.id,))

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Postnatal Follow-Up: Medications"
        verbose_name_plural = "Maternal Postnatal Follow-Up: Medications Items"
