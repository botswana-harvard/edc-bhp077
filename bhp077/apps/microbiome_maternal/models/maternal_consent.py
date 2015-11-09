from django.db import models

from edc.core.bhp_variables.models import StudySite
from edc.core.identifier.classes import SubjectIdentifier
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.models.base_consent import BaseConsent
from edc_consent.models.fields import (PersonalFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin,
                                       VulnerabilityFieldsMixin, IdentityFieldsMixin)

from .maternal_off_study_mixin import MaternalOffStudyMixin


class MaternalConsent(BaseConsent, MaternalOffStudyMixin, ReviewFieldsMixin,
                      IdentityFieldsMixin, PersonalFieldsMixin,
                      CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    study_site = models.ForeignKey(
        StudySite,
        verbose_name='Site',
        null=True,
        help_text="")

    def __unicode__(self):
        return '{0} {1} {2} ({3})'.format(self.subject_identifier, self.first_name,
                                          self.last_name, self.initials)

    def save(self, *args, **kwargs):
        self.subject_identifier = SubjectIdentifier(site_code=self.study_site.site_code).get_identifier()
        super(MaternalConsent, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.consent_datetime

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Consent'
        verbose_name_plural = 'Maternal Consent'
