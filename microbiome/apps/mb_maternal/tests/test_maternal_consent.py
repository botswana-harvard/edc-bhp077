from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.forms import MaternalConsentForm

from .factories import MaternalEligibilityFactory, MaternalConsentFactory
from edc.subject.registration.models.registered_subject import RegisteredSubject
from django.utils import timezone


class TestMaternalConsent(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        site_rule_groups.autodiscover()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.registered_subject = RegisteredSubject.objects.get(
            pk=self.maternal_eligibility.registered_subject.pk)

    def test_identity_wrong_gender(self):
        """Test that Omang number reflects the correct gender digit."""
        consent = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject)
        consent_form = MaternalConsentForm(data=consent.__dict__)
        errors = ''.join(consent_form.errors.get('__all__'))
        self.assertIn('Identity provided indicates participant is Male.', errors)

    def test_registered_subject_registration_datetime_on_post_save(self):
        self.assertIsNone(self.registered_subject.registration_datetime)
        MaternalConsentFactory(
            consent_datetime=timezone.now(),
            identity='123411234',
            confirm_identity='123411234',
            registered_subject=self.registered_subject)
        registered_subject = RegisteredSubject.objects.get(pk=self.registered_subject.pk)
        self.assertIsNotNone(registered_subject.registration_datetime)
