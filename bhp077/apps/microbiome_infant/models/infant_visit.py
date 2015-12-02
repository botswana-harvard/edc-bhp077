from django.db import models

from edc.subject.visit_tracking.models import BaseVisitTracking

from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.subject.entry.models import Entry
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc_constants.constants import POS, YES, NEW

from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment
from bhp077.apps.microbiome.choices import (VISIT_REASON, INFO_PROVIDER, INFANT_VISIT_STUDY_STATUS,
                                            ALIVE_DEAD_UNKNOWN)

from .infant_birth import InfantBirth
from .infant_off_study_mixin import InfantOffStudyMixin
from bhp077.apps.microbiome.classes.meta_data_mixin import MetaDataMixin


class InfantVisit(MetaDataMixin, InfantOffStudyMixin, BaseVisitTracking, BaseUuidModel):

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

    def model_options(self, app_label, model_name):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=self.appointment)
        return model_options

    def rehash_meta_data(self):
        if self.reason == 'unscheduled':
            self.meta_data_visit_unshceduled(self.appointment)

    @property
    def infant_birth_male(self):
        try:
            return InfantBirth.objects.get(registered_subject=self.appointment.registered_subject, gender='M')
        except InfantBirth.DoesNotExist:
            return False
        return True

    @property
    def maternal_registered_subject(self):
        try:
            return RegisteredSubject.objects.get(
                subject_identifier=self.appointment.registered_subject.relative_identifier)
        except RegisteredSubject.DoesNotExist:
            return False

    @property
    def postnatal_enrollment(self):
        return PostnatalEnrollment.objects.get(registered_subject=self.maternal_registered_subject)

    @property
    def hiv_status_pos_and_evidence_yes(self):
        try:
            PostnatalEnrollment.objects.get(
                registered_subject=self.maternal_registered_subject,
                verbal_hiv_status=POS,
                evidence_hiv_status=YES
            )
        except PostnatalEnrollment.DoesNotExist:
            return False
        return True

    def scheduled_entry_meta_data(self, model_name):
        try:
            sd = ScheduledEntryMetaData.objects.filter(**self.model_options(
                'microbiome_infant', model_name)).first()
            sd.entry_status = NEW
            sd.save()
        except AttributeError:
            pass

    def requistion_entry_meta_data(self, model_name):
        rq = RequisitionMetaData.objects.filter(
            lab_entry__requisition_panel__name='DNA PCR',
            lab_entry__app_label='microbiome_lab',
            lab_entry__model_name=model_name,
            appointment=self.appointment
        )
        if rq:
            rq = rq.first()
            rq.entry_status = NEW
            rq.save()

    def create_additional_maternal_forms_meta(self):
        self.reason = 'off study' if not self.postnatal_enrollment.postnatal_eligible else self.reason
        if self.reason == 'off study':
            entry = Entry.objects.get(
                model_name='infantoffstudy',
                visit_definition_id=self.appointment.visit_definition_id)
            scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                appointment=self.appointment,
                entry=entry,
                registered_subject=self.appointment.registered_subject)
            if not scheduled_meta_data:
                scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                    appointment=self.appointment,
                    entry=entry,
                    registered_subject=self.appointment.registered_subject)
            else:
                scheduled_meta_data = scheduled_meta_data[0]
            scheduled_meta_data.entry_status = NEW
            scheduled_meta_data.save()
        if self.reason == 'death':
            entries = Entry.objects.filter(
                model_name__in=['infantdeath', 'infantoffstudy'],
                visit_definition_id=self.appointment.visit_definition_id)
            for entry in entries:
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                    appointment=self.appointment,
                    entry=entry[0],
                    registered_subject=self.appointment.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                        appointment=self.appointment,
                        entry=entry[0],
                        registered_subject=self.appointment.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = NEW
                scheduled_meta_data.save()

    def update_scheduled_entry_meta_data(self):
        if self.hiv_status_pos_and_evidence_yes:
            if self.appointment.visit_definition.code == '2000':
                self.scheduled_entry_meta_data('infantbirtharv')
            if self.appointment.visit_definition.code in ['2010']:
                self.requistion_entry_meta_data('infantrequisition')
        if self.appointment.visit_definition.code in ['2030', '2060', '2090', '2120']:
            if self.infant_birth_male:
                self.scheduled_entry_meta_data('infantcircumcision')

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def save(self, *args, **kwargs):
        self.create_additional_maternal_forms_meta()
        super(InfantVisit, self).save(*args, **kwargs)

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
