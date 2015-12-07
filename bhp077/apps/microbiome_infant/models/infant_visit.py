from django.db import models

from edc.subject.visit_tracking.models import BaseVisitTracking

from edc_base.audit_trail import AuditTrail
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.subject.entry.models import Entry
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc_constants.constants import POS, YES, NEW, MALE, UNSCHEDULED

from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment
from bhp077.apps.microbiome.choices import (VISIT_REASON, INFO_PROVIDER, INFANT_VISIT_STUDY_STATUS,
                                            ALIVE_DEAD_UNKNOWN)

from .infant_birth import InfantBirth
from .infant_off_study_mixin import InfantOffStudyMixin


class InfantVisit(InfantOffStudyMixin, BaseVisitTracking, BaseUuidModel):

    """ A model completed by the user on the infant visits. """

    information_provider = models.CharField(
        verbose_name="Please indicate who provided most of the information for this child's visit",
        choices=INFO_PROVIDER,
        max_length=20,
        help_text="")

    information_provider_other = models.CharField(
        verbose_name="if information provider is Other, please specify",
        max_length=20,
        help_text="",
        blank=True,
        null=True)

    study_status = models.CharField(
        verbose_name="What is the participant's current study status",
        max_length=50,
        choices=INFANT_VISIT_STUDY_STATUS)

    survival_status = models.CharField(
        max_length=10,
        verbose_name="Survival status",
        choices=ALIVE_DEAD_UNKNOWN,
        null=True,
        blank=False)

    date_last_alive = models.DateField(
        verbose_name="Date last known alive",
        help_text="",
        null=True,
        blank=True)

    objects = models.Manager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.reason = 'off study' if not self.get_postnatal_enrollment().is_eligible else self.reason
        super(InfantVisit, self).save(*args, **kwargs)

    def get_postnatal_enrollment(self):
        maternal_registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.appointment.registered_subject.relative_identifier)
        return PostnatalEnrollment.objects.get(registered_subject=maternal_registered_subject)

    @property
    def hiv_status_pos_and_evidence_yes(self):
        maternal_registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.appointment.registered_subject.relative_identifier)
        try:
            PostnatalEnrollment.objects.get(
                registered_subject=maternal_registered_subject,
                current_hiv_status=POS,
                evidence_hiv_status=YES
            )
        except PostnatalEnrollment.DoesNotExist:
            return False
        return True

    def form_is_required(self, app_label, model_name):
        """Sets a form to NEW if not already NEW (scheduled_entry_meta_data)."""
        scheduled_entry_meta_data = ScheduledEntryMetaData.objects.get(
            app_label=app_label,
            model_name=model_name,
            appointment=self.appointment)
        if scheduled_entry_meta_data.entry_status != NEW:
            scheduled_entry_meta_data.entry_status = NEW
            scheduled_entry_meta_data.save()

    def requisition_is_required(self, model_name, panel_name):
        """Sets a requisition to NEW if not already NEW (requisition_meta_data)."""
        requisition_meta_data = RequisitionMetaData.objects.get(
            lab_entry__requisition_panel__name=panel_name,
            lab_entry__app_label='microbiome_lab',
            lab_entry__model_name=model_name,
            appointment=self.appointment
        )
        if requisition_meta_data.entry_status == NEW:
            requisition_meta_data.entry_status = NEW
            requisition_meta_data.save()

    def update_scheduled_entry_meta_data(self):
        if self.reason == UNSCHEDULED:
            self.meta_data_visit_unscheduled(self.appointment)
        if self.hiv_status_pos_and_evidence_yes:
            if self.appointment.visit_definition.code == '2000':
                self.form_is_required(self.app_label, 'infantbirtharv')
            if self.appointment.visit_definition.code in ['2010']:
                self.requistion_is_required('infantrequisition', 'DNA PCR')
        if self.appointment.visit_definition.code in ['2030', '2060', '2090', '2120']:
            try:
                InfantBirth.objects.get(
                    registered_subject=self.appointment.registered_subject, gender=MALE)
                self.form_is_required(self.app_label, 'infantcircumcision')
            except InfantBirth.DoesNotExist:
                pass

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
