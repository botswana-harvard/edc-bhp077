from django.db import models

from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin

from maternal_off_study_mixin import MaternalOffStudyMixin


class MaternalVisit(MaternalOffStudyMixin, RequiresConsentMixin, BaseVisitTracking, BaseUuidModel):

    """ Maternal visit form that links all antenatal/ postnatal follow-up forms """

    history = AuditTrail(True)

    def __unicode__(self):
        return '{} {} ({}) {}'.format(self.appointment.registered_subject.subject_identifier,
                                      self.appointment.registered_subject.first_name,
                                      self.appointment.registered_subject.gender,
                                      self.appointment.visit_definition.code)

    class Meta:
        app_label = 'maternal'
        verbose_name = 'Maternal Visit'
        verbose_name_plural = 'Maternal Visit'
