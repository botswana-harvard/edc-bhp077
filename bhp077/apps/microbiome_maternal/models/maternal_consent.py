from django.db import models

from edc.core.bhp_variables.models import StudySite
from edc.core.identifier.classes import SubjectIdentifier
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.models.base_consent import BaseConsent
from edc_consent.models.fields import (PersonalFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin,
                                       VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin

from .maternal_off_study_mixin import MaternalOffStudyMixin
from ..maternal_choices import RECRUIT_SOURCE, RECRUIT_CLINIC, SITE
from django.template.defaultfilters import default


class MaternalConsent(BaseConsent, MaternalOffStudyMixin, ReviewFieldsMixin,
                      IdentityFieldsMixin, PersonalFieldsMixin,
                      CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    study_site = models.ForeignKey(
        StudySite,
    )

#     study_site = models.CharField(
#         verbose_name='Site',
#         choices=SITE,
#         default='Gaborone',
#         max_length=10,
#         null=True,
#         help_text="")
#
#     site_code = models.IntegerField(
#         verbose_name='Site',
#         default=40,
#         max_length=10,
#         null=True,
#         help_text="")

    recruit_source = models.CharField(
        max_length=75,
        choices=RECRUIT_SOURCE,
        verbose_name="The mother first learned about the Microbiome study from ",
        help_text="", )
    recruit_source_other = OtherCharField(
        max_length=35,
        verbose_name="if other recruitment source, specify...",
        blank=True,
        null=True, )
    recruitment_clinic = models.CharField(
        max_length=100,
        verbose_name="The mother was recruited from",
        choices=RECRUIT_CLINIC, )
    recruitment_clinic_other = models.CharField(
        max_length=100,
        verbose_name="if other recruitment clinic, specify...",
        blank=True,
        null=True, )

    def __unicode__(self):
        return '{0} {1} {2} ({3})'.format(self.subject_identifier, self.first_name,
                                          self.last_name, self.initials)

    def save(self, *args, **kwargs):
        self.subject_identifier = SubjectIdentifier(site_code=self.study_site.site_code).get_identifier()
        self.gender = self.maternal_eligibility.registered_subject.gender
        super(MaternalConsent, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.consent_datetime

    @property
    def maternal_eligibility(self):
        from bhp077.apps.microbiome_maternal.models import MaternalEligibility
        maternal_eligibility = MaternalEligibility.objects.get(registered_subject=self.registered_subject)
        return maternal_eligibility

    history = AuditTrail()

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Consent'
        verbose_name_plural = 'Maternal Consent'
