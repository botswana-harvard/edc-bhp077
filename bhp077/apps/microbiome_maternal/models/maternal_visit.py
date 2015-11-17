from django.core.urlresolvers import reverse
from django.db import models

from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.entry.models import Entry
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import NEW, YES, POS
from edc.subject.visit_tracking.settings import VISIT_REASON_NO_FOLLOW_UP_CHOICES

from .maternal_off_study_mixin import MaternalOffStudyMixin
from bhp077.apps.microbiome.choices import VISIT_UNSCHEDULED_REASON, VISIT_REASON
from bhp077.apps.microbiome_maternal.models import MaternalConsent, PostnatalEnrollment


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

    @property
    def postnatal_enrollment(self):
        return PostnatalEnrollment.objects.get(registered_subject=self.appointment.registered_subject)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        self.create_additional_maternal_forms_meta()
        super(MaternalVisit, self).save(*args, **kwargs)

    def model_options(self, app_label, model_name):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=self.appointment)
        return model_options

    def get_visit_reason_no_follow_up_choices(self):
        """Returns the visit reasons that do not imply any data collection; that is, the subject is not available."""
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
            dct.update({'vital status': 'Vital Status'})
        del dct['death']
        del dct['lost']
        return dct

    @property
    def hiv_rapid_test_pos(self):
        try:
            PostnatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject,
                process_rapid_test=YES,
                rapid_test_result=POS
            )
        except PostnatalEnrollment.DoesNotExist:
            return False
        return True

    @property
    def hiv_status_pos_and_evidence_yes(self):
        try:
            PostnatalEnrollment.objects.get(
                registered_subject=self.appointment.registered_subject,
                verbal_hiv_status=POS,
                evidence_hiv_status=YES
            )
        except PostnatalEnrollment.DoesNotExist:
            return False
        return True

    def scheduled_entry_meta_data(self, model_name):
        sd = ScheduledEntryMetaData.objects.filter(**self.model_options(
            'microbiome_maternal', model_name)).first()
        sd.entry_status = NEW
        sd.save()

    def update_scheduled_entry_meta_data(self):
        if self.hiv_status_pos_and_evidence_yes:
            if self.appointment.visit_definition.code == '1000M':
                for model_name in ['maternalinfected', 'maternalarvhistory', 'maternalarvpreg', 'maternalclinicalhistory']:
                    self.scheduled_entry_meta_data(model_name)
            elif self.appointment.visit_definition.code == '2000M':
                for model_name in ['maternalarvpreg', 'maternallabdelclinic']:
                    self.scheduled_entry_meta_data(model_name)
            elif self.appointment.visit_definition.code in ['2010M', '2030M', '2060M', '2090M', '2120M']:
                self.scheduled_entry_meta_data('maternalarvpost')
        else:
            pass

    def create_additional_maternal_forms_meta(self):
        self.reason = 'off study' if not self.postnatal_enrollment.postnatal_eligible else self.reason
        if self.reason == 'off study':
            entry = Entry.objects.filter(
                model_name='maternaloffstudy',
                visit_definition_id=self.appointment.visit_definition_id)
            if entry:
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
                scheduled_meta_data.entry_status = 'NEW'
                scheduled_meta_data.save()
        if self.reason == 'death':
            entries = Entry.objects.filter(
                model_name__in=['maternaldeath', 'maternaloffstudy'],
                visit_definition_id=self.appointment.visit_definition_id)
            for entry in entries:
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

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Visit'
        verbose_name_plural = 'Maternal Visit'
