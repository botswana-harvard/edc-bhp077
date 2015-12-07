from django.db import models

from edc.subject.visit_tracking.models import BaseVisitTracking

from edc_base.audit_trail import AuditTrail
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.entry.models import Entry
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc_constants.constants import UNSCHEDULED, OFF_STUDY

from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment
from bhp077.apps.microbiome.choices import (VISIT_REASON, INFO_PROVIDER, INFANT_VISIT_STUDY_STATUS,
                                            ALIVE_DEAD_UNKNOWN)

from .infant_birth import InfantBirth
from .infant_off_study_mixin import InfantOffStudyMixin
from bhp077.apps.microbiome.classes.meta_data_mixin import MetaDataMixin
from edc.constants import DEAD


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

    objects = models.Manager()

    history = AuditTrail()

    def model_options(self, app_label, model_name):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=self.appointment)
        return model_options

    def update_entry_meta_data(self):
        if self.reason == UNSCHEDULED:
            self.meta_data_visit_unscheduled(self.appointment)

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

    def infant_offstudy_required(self):
        self.reason = OFF_STUDY if not self.postnatal_enrollment.postnatal_eligible else self.reason
        if self.reason == OFF_STUDY:
            self.scheduled_entry_meta_data_required('microbiome_infant', 'infantoffstudy')

    def infant_death_required(self):
        if self.reason == DEAD:
            for model_name in ['infantdeath', 'infantoffstudy']:
                self.scheduled_entry_meta_data_required('microbiome_infant', model_name)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def update_required_forms_on_post_save(self):
        if self.postnatal_enrollment.maternal_hiv_status:
            if self.appointment.visit_definition.code == '2000':
                self.scheduled_entry_meta_data_required('microbiome_infant', 'infantbirtharv')
            if self.appointment.visit_definition.code in ['2010', '2030', '2060', '2090', '2120']:
                self.requisition_is_required('infantrequisition', 'DNA PCR')

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Visit"
        verbose_name_plural = "Infant Visit"
