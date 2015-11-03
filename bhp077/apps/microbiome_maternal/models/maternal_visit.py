from django.core.urlresolvers import reverse
from django.db import models

from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_base.model.models import BaseUuidModel
from edc_base.audit_trail import AuditTrail
from edc_consent.models import RequiresConsentMixin
from bhp077.apps.microbiome_maternal.models import MaternalConsent

from bhp077.apps.microbiome.choices import VISIT_UNSCHEDULED_REASON, VISIT_REASON
from .maternal_off_study_mixin import MaternalOffStudyMixin


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
        return '{} {} ({}) {}'.format(self.appointment.registered_subject.subject_identifier,
                                      self.appointment.registered_subject.first_name,
                                      self.appointment.registered_subject.gender,
                                      self.appointment.visit_definition.code)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        super(MaternalVisit, self).save(*args, **kwargs)

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Visit'
        verbose_name_plural = 'Maternal Visit'
