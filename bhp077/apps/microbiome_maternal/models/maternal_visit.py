from django.core.urlresolvers import reverse
from django.db import models

from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.entry.models import Entry
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin

from .maternal_off_study_mixin import MaternalOffStudyMixin
from bhp077.apps.microbiome.choices import VISIT_UNSCHEDULED_REASON, VISIT_REASON
from bhp077.apps.microbiome_maternal.models import MaternalConsent


class MaternalVisit(MaternalOffStudyMixin, RequiresConsentMixin, BaseVisitTracking, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    CONSENT_MODEL = MaternalConsent

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON)

    history = AuditTrail(True)

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternalvisit_add', args=(self.id,))

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        self.create_additional_maternal_forms_meta()
        super(MaternalVisit, self).save(*args, **kwargs)

    def create_additional_maternal_forms_meta(self):
        if self.reason == 'off study':
            entry = Entry.objects.filter(
                model_name='maternaloffstudy',
                visit_definition_id=self.appointment.visit_definition_id)
            if entry:
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                    appointment=self.appointment,
                    entry=entry[0],
                    registered_subject=self.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                        appointment=self.appointment,
                        entry=entry[0],
                        registered_subject=self.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = 'NEW'
                scheduled_meta_data.save()
        if self.reason == 'death':
            entries = Entry.objects.filter(
                model_name__in=['maternaldeath', 'maternaloffstudy'],
                visit_definition_id=self.appointment.visit_definition_id)
            for entry in entries:
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                    appointment=self.appointment,
                    entry=entry[0],
                    registered_subject=self.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                        appointment=self.appointment,
                        entry=entry[0],
                        registered_subject=self.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = 'NEW'
                scheduled_meta_data.save()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Visit'
        verbose_name_plural = 'Maternal Visit'
