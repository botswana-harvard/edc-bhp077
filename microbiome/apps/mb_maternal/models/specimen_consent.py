from django.db import models

from edc.device.sync.models import BaseSyncUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc_appointment.models import AppointmentMixin
from edc_base.audit_trail import AuditTrail
from edc_consent.models import RequiresConsentMixin, BaseSpecimenConsent
from edc_consent.models.fields import SampleCollectionFieldsMixin, VulnerabilityFieldsMixin

from ..managers import SpecimenConsentManager

from .maternal_consent import MaternalConsent


class SpecimenConsent(BaseSpecimenConsent, SampleCollectionFieldsMixin, RequiresConsentMixin,
                      VulnerabilityFieldsMixin, AppointmentMixin, BaseSyncUuidModel):

    """ A model completed by the user when a mother gives consent for specimen storage. """

    consent_model = MaternalConsent

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    objects = SpecimenConsentManager()

    history = AuditTrail()

    def __unicode__(self):
        return "{0}".format(self.registered_subject.subject_identifier)

    def natural_key(self):
        return self.registered_subject.natural_key()

    def prepare_appointments(self, using):
        """Overrides so that the signal does not attempt to prepare appointments."""
        pass

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.consent_datetime

    @property
    def report_datetime(self):
        return self.consent_datetime

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Specimen Consent'
        verbose_name_plural = 'Specimen Consent'
